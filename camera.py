"""
camera.py  –  Live pose detection + push-up rep counter using MediaPipe & OpenCV.
The generate_frames() function is a generator consumed by Flask's Response object.
"""

import cv2
import numpy as np

# MediaPipe setup
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
# ── Shared state (simple globals for this beginner project) ───────────────────
_rep_count = 0
_stage     = None   # "up" | "down"

def get_rep_count():
    return _rep_count

def reset_rep_count():
    global _rep_count, _stage
    _rep_count = 0
    _stage     = None

# ── Geometry helper ────────────────────────────────────────────────────────────

def calculate_angle(a, b, c):
    """Return the angle (degrees) at point b formed by vectors b→a and b→c."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle  = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return angle

# ── Frame generator ────────────────────────────────────────────────────────────

def generate_frames():
    """
    Yields MJPEG frames for Flask's multipart/x-mixed-replace response.
    Counts push-up reps by tracking the left-elbow angle.
    """
    global _rep_count, _stage

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                # Yield a blank frame so the stream doesn't drop
                blank = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(blank, 'Camera not available', (120, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                _, buf = cv2.imencode('.jpg', blank)
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n'
                break

            # Convert BGR → RGB for MediaPipe
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results = pose.process(rgb)

            # Convert back to BGR for drawing
            image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            image.flags.writeable = True

            angle = None

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                h, w = image.shape[:2]

                # -- Get key-point coordinates (normalised → pixel) --------------
                def pt(idx):
                    p = lm[idx]
                    return [p.x, p.y]   # keep normalised for angle calc

                shoulder = pt(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
                elbow    = pt(mp_pose.PoseLandmark.LEFT_ELBOW.value)
                wrist    = pt(mp_pose.PoseLandmark.LEFT_WRIST.value)

                angle = calculate_angle(shoulder, elbow, wrist)

                # -- Push-up rep logic -------------------------------------------
                # "up"  = arms extended  (angle > 160°)
                # "down" = chest near ground (angle < 70°)
                if angle > 160:
                    _stage = "up"
                if angle < 70 and _stage == "up":
                    _stage = "down"
                    _rep_count += 1

                # -- Draw angle near elbow ---------------------------------------
                elbow_px = (int(elbow[0] * w), int(elbow[1] * h))
                cv2.putText(image, f'{int(angle)}\xb0', elbow_px,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                # -- Draw skeleton -----------------------------------------------
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0, 255, 180), thickness=2, circle_radius=3),
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(255, 100, 0), thickness=2)
                )

            # -- HUD overlay (top-left box) ---------------------------------------
            cv2.rectangle(image, (0, 0), (260, 80), (15, 15, 35), -1)

            cv2.putText(image, 'REPS',  (12, 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (160, 160, 160), 1)
            cv2.putText(image, str(_rep_count), (12, 68),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 220, 255), 3)

            cv2.putText(image, 'STAGE', (100, 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (160, 160, 160), 1)
            stage_text = (_stage or 'N/A').upper()
            cv2.putText(image, stage_text, (95, 68),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 150), 2)

            if angle is not None:
                cv2.putText(image, f'ANGLE {int(angle)}', (170, 68),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 220, 0), 2)

            # Exercise label
            cv2.putText(image, 'EXERCISE: PUSH-UP', (10, image.shape[0] - 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

            # -- Encode and yield ------------------------------------------------
            ret, buf = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + buf.tobytes()
                   + b'\r\n')

    cap.release()
