# import cv2
# import pygame
# import numpy as np
# import sys
# import time

# # --- CONFIGURATION & COLORS ---
# VIDEO_SIZE = 600        # The puzzle area (Square)
# UI_WIDTH = 250          # The side panel width
# WINDOW_WIDTH = VIDEO_SIZE + UI_WIDTH
# WINDOW_HEIGHT = VIDEO_SIZE
# GRID_SIZE = 4           # 4x4 Grid
# TILE_SIZE = VIDEO_SIZE // GRID_SIZE
# FPS = 60
# TIME_LIMIT = 60         # Seconds to solve

# # Cyberpunk Palette
# COLOR_BG = (10, 15, 20)           # Deep Dark Blue/Black
# COLOR_ACCENT = (0, 240, 255)      # Cyan Neon
# COLOR_SUCCESS = (50, 255, 50)     # Bright Green
# COLOR_FAIL = (255, 50, 50)        # Bright Red
# COLOR_TEXT = (220, 220, 220)      # Off White
# COLOR_GRID_LINES = (0, 0, 0)

# class LiveJigsawCaptcha:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#         pygame.display.set_caption("IDENTITY VERIFICATION // LIVE CAPTCHA")
#         self.clock = pygame.time.Clock()
        
#         # Fonts
#         self.font_header = pygame.font.SysFont("Consolas", 28, bold=True)
#         self.font_body = pygame.font.SysFont("Consolas", 18)
#         self.font_big = pygame.font.SysFont("Consolas", 50, bold=True)

#         # Camera Setup
#         self.cap = cv2.VideoCapture(0)
        
#         # Game States: 'MENU', 'PLAYING', 'WON', 'LOST'
#         self.state = 'MENU'
        
#         # Logic Variables
#         self.correct_order = list(range(GRID_SIZE * GRID_SIZE))
#         self.current_order = self.correct_order.copy()
        
#         self.selected_tile = None
#         self.dragging = False
#         self.mouse_offset = (0, 0)
        
#         self.start_time = 0
#         self.elapsed_time = 0

#         # UI Rectangles
#         self.btn_rect = pygame.Rect(VIDEO_SIZE + 25, WINDOW_HEIGHT - 100, 200, 50)

#     def shuffle_grid(self):
#         """Shuffles the grid for gameplay."""
#         import random
#         random.shuffle(self.current_order)

#     def get_live_frame(self):
#         """Captures, mirrors, resizes, and formats the frame."""
#         ret, frame = self.cap.read()
#         if not ret: return None
        
#         frame = cv2.flip(frame, 1) # Mirror
#         frame = cv2.resize(frame, (VIDEO_SIZE, VIDEO_SIZE)) # Resize to 600x600
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR to RGB
        
#         # Rotate for Pygame surface compatibility
#         return np.rot90(frame)

#     def draw_sidebar(self):
#         """Draws the UI panel on the right."""
#         # Background for sidebar
#         pygame.draw.rect(self.screen, COLOR_BG, (VIDEO_SIZE, 0, UI_WIDTH, WINDOW_HEIGHT))
#         pygame.draw.line(self.screen, COLOR_ACCENT, (VIDEO_SIZE, 0), (VIDEO_SIZE, WINDOW_HEIGHT), 2)

#         # Header Text
#         title = self.font_header.render("SECURITY", True, COLOR_ACCENT)
#         subtitle = self.font_header.render("PROTOCOL", True, COLOR_ACCENT)
#         self.screen.blit(title, (VIDEO_SIZE + 20, 30))
#         self.screen.blit(subtitle, (VIDEO_SIZE + 20, 60))

#         # Status Display
#         status_text = "STATUS:"
#         if self.state == 'MENU': status_val = "WAITING"
#         elif self.state == 'PLAYING': status_val = "SCANNING..."
#         elif self.state == 'WON': status_val = "VERIFIED"
#         else: status_val = "DENIED"
        
#         color = COLOR_SUCCESS if self.state == 'WON' else (COLOR_FAIL if self.state == 'LOST' else COLOR_TEXT)
        
#         self.screen.blit(self.font_body.render(status_text, True, COLOR_TEXT), (VIDEO_SIZE + 20, 120))
#         self.screen.blit(self.font_body.render(status_val, True, color), (VIDEO_SIZE + 20, 145))

#         # Timer Logic (Only in PLAYING state)
#         if self.state == 'PLAYING':
#             remaining = max(0, TIME_LIMIT - int(self.elapsed_time))
#             timer_color = COLOR_FAIL if remaining < 10 else COLOR_ACCENT
            
#             # Text Timer
#             time_surf = self.font_big.render(f"00:{remaining:02}", True, timer_color)
#             self.screen.blit(time_surf, (VIDEO_SIZE + 20, 200))
            
#             # Bar Timer
#             bar_width = 200
#             fill_width = int((remaining / TIME_LIMIT) * bar_width)
#             pygame.draw.rect(self.screen, (50,50,50), (VIDEO_SIZE + 25, 260, bar_width, 10))
#             pygame.draw.rect(self.screen, timer_color, (VIDEO_SIZE + 25, 260, fill_width, 10))
            
#             if remaining == 0:
#                 self.state = 'LOST'

#         # Start / Reset Button
#         mx, my = pygame.mouse.get_pos()
#         hover = self.btn_rect.collidepoint((mx, my))
        
#         btn_color = COLOR_ACCENT if hover else (50, 50, 50)
#         text_color = (0,0,0) if hover else COLOR_TEXT
#         btn_text = "RESET SYSTEM" if self.state in ['WON', 'LOST'] else "INITIATE"
        
#         if self.state != 'PLAYING':
#             pygame.draw.rect(self.screen, btn_color, self.btn_rect)
#             pygame.draw.rect(self.screen, COLOR_ACCENT, self.btn_rect, 2) # Border
            
#             lbl = self.font_body.render(btn_text, True, text_color)
#             # Center text in button
#             lbl_x = self.btn_rect.x + (self.btn_rect.width - lbl.get_width()) // 2
#             lbl_y = self.btn_rect.y + (self.btn_rect.height - lbl.get_height()) // 2
#             self.screen.blit(lbl, (lbl_x, lbl_y))

#     def run(self):
#         running = True
#         while running:
#             # 1. Capture & Process Video
#             frame_rgb = self.get_live_frame()
#             if frame_rgb is None: break
            
#             full_surf = pygame.surfarray.make_surface(frame_rgb)
            
#             # 2. Input Handling
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
                
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     if event.button == 1:
#                         mx, my = event.pos
                        
#                         # Handle Button Click (Start/Reset)
#                         if self.state != 'PLAYING' and self.btn_rect.collidepoint((mx, my)):
#                             self.state = 'PLAYING'
#                             self.shuffle_grid()
#                             self.start_time = time.time()
#                             continue

#                         # Handle Puzzle Click (Only if Playing)
#                         if self.state == 'PLAYING' and mx < VIDEO_SIZE:
#                             col = mx // TILE_SIZE
#                             row = my // TILE_SIZE
#                             index = row * GRID_SIZE + col
#                             self.dragging = True
#                             self.selected_tile = index
#                             self.mouse_offset = (mx - col * TILE_SIZE, my - row * TILE_SIZE)

#                 elif event.type == pygame.MOUSEBUTTONUP:
#                     if event.button == 1 and self.dragging:
#                         # Drop Logic
#                         mx, my = event.pos
#                         if mx < VIDEO_SIZE: # Ensure drop is inside game area
#                             t_col = mx // TILE_SIZE
#                             t_row = my // TILE_SIZE
#                             t_index = t_row * GRID_SIZE + t_col
                            
#                             # Swap
#                             if self.selected_tile is not None:
#                                 self.current_order[self.selected_tile], self.current_order[t_index] = \
#                                 self.current_order[t_index], self.current_order[self.selected_tile]
                                
#                                 # Check Win Condition
#                                 if self.current_order == self.correct_order:
#                                     self.state = 'WON'

#                         self.dragging = False
#                         self.selected_tile = None

#             # 3. Logic Updates
#             if self.state == 'PLAYING':
#                 self.elapsed_time = time.time() - self.start_time

#             # 4. Drawing Phase
#             self.screen.fill((0,0,0))
            
#             # --- Draw the Video Puzzle ---
#             if self.state == 'MENU':
#                 # Show Unscrambled Preview
#                 self.screen.blit(full_surf, (0,0))
#                 # Add a dark overlay
#                 s = pygame.Surface((VIDEO_SIZE, VIDEO_SIZE))
#                 s.set_alpha(100)
#                 s.fill((0,0,0))
#                 self.screen.blit(s, (0,0))
                
#             else:
#                 # Draw Scrambled/Playing Grid
#                 for i in range(16):
#                     if self.dragging and i == self.selected_tile: continue # Draw dragged piece last

#                     # Draw Position
#                     dx = (i % GRID_SIZE) * TILE_SIZE
#                     dy = (i // GRID_SIZE) * TILE_SIZE
                    
#                     # Source Position (from video)
#                     val = self.current_order[i]
#                     sx = (val % GRID_SIZE) * TILE_SIZE
#                     sy = (val // GRID_SIZE) * TILE_SIZE
                    
#                     self.screen.blit(full_surf, (dx, dy), (sx, sy, TILE_SIZE, TILE_SIZE))
#                     pygame.draw.rect(self.screen, COLOR_GRID_LINES, (dx, dy, TILE_SIZE, TILE_SIZE), 1)

#             # --- Draw Dragged Piece (Floating) ---
#             if self.dragging and self.selected_tile is not None:
#                 mx, my = pygame.mouse.get_pos()
#                 val = self.current_order[self.selected_tile]
#                 sx = (val % GRID_SIZE) * TILE_SIZE
#                 sy = (val // GRID_SIZE) * TILE_SIZE
                
#                 self.screen.blit(full_surf, (mx - self.mouse_offset[0], my - self.mouse_offset[1]), (sx, sy, TILE_SIZE, TILE_SIZE))
#                 pygame.draw.rect(self.screen, COLOR_ACCENT, (mx - self.mouse_offset[0], my - self.mouse_offset[1], TILE_SIZE, TILE_SIZE), 3)

#             # --- Draw Side Panel ---
#             self.draw_sidebar()

#             # --- Game Over / Win Overlays on Video ---
#             if self.state == 'WON':
#                 pygame.draw.rect(self.screen, COLOR_SUCCESS, (0, 0, VIDEO_SIZE, VIDEO_SIZE), 5)
#                 msg = self.font_big.render("ACCESS GRANTED", True, COLOR_SUCCESS)
#                 self.screen.blit(msg, (VIDEO_SIZE//2 - msg.get_width()//2, VIDEO_SIZE//2))
            
#             elif self.state == 'LOST':
#                 pygame.draw.rect(self.screen, COLOR_FAIL, (0, 0, VIDEO_SIZE, VIDEO_SIZE), 5)
#                 msg = self.font_big.render("ACCESS DENIED", True, COLOR_FAIL)
#                 self.screen.blit(msg, (VIDEO_SIZE//2 - msg.get_width()//2, VIDEO_SIZE//2))

#             pygame.display.flip()
#             self.clock.tick(FPS)

#         self.cap.release()
#         pygame.quit()
#         sys.exit()

# if __name__ == "__main__":
#     game = LiveJigsawCaptcha()
#     game.run()

import cv2
import pygame
import numpy as np
import sys
import time
import mediapipe as mp
import math

# --- CONFIGURATION & COLORS ---
VIDEO_SIZE = 600        # The puzzle area (Square)
UI_WIDTH = 250          # The side panel width
WINDOW_WIDTH = VIDEO_SIZE + UI_WIDTH
WINDOW_HEIGHT = VIDEO_SIZE
GRID_SIZE = 4           # 4x4 Grid
TILE_SIZE = VIDEO_SIZE // GRID_SIZE
FPS = 60
TIME_LIMIT = 60         # Seconds to solve

# Cyberpunk Palette
COLOR_BG = (10, 15, 20)           # Deep Dark Blue/Black
COLOR_ACCENT = (0, 240, 255)      # Cyan Neon
COLOR_SUCCESS = (50, 255, 50)     # Bright Green
COLOR_FAIL = (255, 50, 50)        # Bright Red
COLOR_TEXT = (220, 220, 220)      # Off White
COLOR_GRID_LINES = (0, 0, 0)
COLOR_HAND_CURSOR = (255, 0, 255) # Magenta for hand cursor

class LiveJigsawCaptcha:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("IDENTITY VERIFICATION // LIVE CAPTCHA + GESTURES")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_header = pygame.font.SysFont("Consolas", 28, bold=True)
        self.font_body = pygame.font.SysFont("Consolas", 18)
        self.font_big = pygame.font.SysFont("Consolas", 50, bold=True)

        # Camera Setup
        self.cap = cv2.VideoCapture(0)
        
        # --- MEDIAPIPE HAND SETUP ---
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Game States: 'MENU', 'PLAYING', 'WON', 'LOST'
        self.state = 'MENU'
        
        # Logic Variables
        self.correct_order = list(range(GRID_SIZE * GRID_SIZE))
        self.current_order = self.correct_order.copy()
        
        self.selected_tile = None
        self.dragging = False
        self.mouse_offset = (0, 0)
        
        # Hand Interaction State
        self.hand_cursor_pos = None  # (x, y)
        self.is_pinching = False
        self.was_pinching = False    # To detect state changes
        
        self.start_time = 0
        self.elapsed_time = 0

        # UI Rectangles
        self.btn_rect = pygame.Rect(VIDEO_SIZE + 25, WINDOW_HEIGHT - 100, 200, 50)

    def shuffle_grid(self):
        import random
        random.shuffle(self.current_order)

    def get_live_frame_and_hands(self):
        """Captures frame, processes hands, returns Pygame surface + hand pos."""
        ret, frame = self.cap.read()
        if not ret: return None, None, False

        # 1. Flip and Resize Standard
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (VIDEO_SIZE, VIDEO_SIZE))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 2. Process Hands (MediaPipe works on the RGB image)
        results = self.hands.process(frame_rgb)
        
        hand_pos = None # Default to None if no hand found
        pinching = False

        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0]
            h, w, c = frame.shape
            
            # Get Raw Coordinates (0.0 - 1.0) -> Pixels
            ix, iy = int(lm.landmark[8].x * w), int(lm.landmark[8].y * h)
            tx, ty = int(lm.landmark[4].x * w), int(lm.landmark[4].y * h)
            
            # Pinch Detection
            distance = math.hypot(ix - tx, iy - ty)
            if distance < 40:
                pinching = True
            
            # COORDINATE MAPPING FOR PYGAME
            # We are about to rotate the image 90 degrees CCW for Pygame.
            # We must map the hand coordinates to match that rotation.
            # Formula: New_X = Old_Y, New_Y = Width - Old_X
            mapped_x = iy
            mapped_y = VIDEO_SIZE - ix
            
            hand_pos = (mapped_x, mapped_y)

        # 3. Rotate Image for Pygame Display
        # np.rot90 rotates 90 deg counter-clockwise
        frame_rotated = np.rot90(frame_rgb)
        
        return frame_rotated, hand_pos, pinching

    def draw_sidebar(self):
        """Draws the UI panel on the right."""
        pygame.draw.rect(self.screen, COLOR_BG, (VIDEO_SIZE, 0, UI_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(self.screen, COLOR_ACCENT, (VIDEO_SIZE, 0), (VIDEO_SIZE, WINDOW_HEIGHT), 2)

        # Header
        title = self.font_header.render("SECURITY", True, COLOR_ACCENT)
        subtitle = self.font_header.render("PROTOCOL", True, COLOR_ACCENT)
        self.screen.blit(title, (VIDEO_SIZE + 20, 30))
        self.screen.blit(subtitle, (VIDEO_SIZE + 20, 60))

        # Status
        status_text = "STATUS:"
        if self.state == 'MENU': status_val = "WAITING"
        elif self.state == 'PLAYING': status_val = "SCANNING..."
        elif self.state == 'WON': status_val = "VERIFIED"
        else: status_val = "DENIED"
        
        color = COLOR_SUCCESS if self.state == 'WON' else (COLOR_FAIL if self.state == 'LOST' else COLOR_TEXT)
        self.screen.blit(self.font_body.render(status_text, True, COLOR_TEXT), (VIDEO_SIZE + 20, 120))
        self.screen.blit(self.font_body.render(status_val, True, color), (VIDEO_SIZE + 20, 145))
        
        # Control Mode Indicator
        mode_txt = "INPUT: MOUSE + HAND"
        self.screen.blit(self.font_body.render(mode_txt, True, (150, 150, 150)), (VIDEO_SIZE + 20, 175))

        # Timer
        if self.state == 'PLAYING':
            remaining = max(0, TIME_LIMIT - int(self.elapsed_time))
            timer_color = COLOR_FAIL if remaining < 10 else COLOR_ACCENT
            time_surf = self.font_big.render(f"00:{remaining:02}", True, timer_color)
            self.screen.blit(time_surf, (VIDEO_SIZE + 20, 200))
            
            bar_width = 200
            fill_width = int((remaining / TIME_LIMIT) * bar_width)
            pygame.draw.rect(self.screen, (50,50,50), (VIDEO_SIZE + 25, 260, bar_width, 10))
            pygame.draw.rect(self.screen, timer_color, (VIDEO_SIZE + 25, 260, fill_width, 10))
            
            if remaining == 0: self.state = 'LOST'

        # Button
        mx, my = pygame.mouse.get_pos()
        # Overwrite mouse pos if hand is active and hovering button
        if self.hand_cursor_pos:
            mx, my = self.hand_cursor_pos
            
        hover = self.btn_rect.collidepoint((mx, my))
        btn_color = COLOR_ACCENT if hover else (50, 50, 50)
        btn_text = "RESET SYSTEM" if self.state in ['WON', 'LOST'] else "INITIATE"
        
        if self.state != 'PLAYING':
            pygame.draw.rect(self.screen, btn_color, self.btn_rect)
            pygame.draw.rect(self.screen, COLOR_ACCENT, self.btn_rect, 2)
            lbl = self.font_body.render(btn_text, True, (0,0,0) if hover else COLOR_TEXT)
            lbl_x = self.btn_rect.x + (self.btn_rect.width - lbl.get_width()) // 2
            lbl_y = self.btn_rect.y + (self.btn_rect.height - lbl.get_height()) // 2
            self.screen.blit(lbl, (lbl_x, lbl_y))

    def handle_input_logic(self, input_pos, is_click_start, is_click_release, is_holding):
        """Unified logic for both Mouse and Hand inputs."""
        mx, my = input_pos
        
        # Button Logic
        if is_click_start:
            if self.state != 'PLAYING' and self.btn_rect.collidepoint((mx, my)):
                self.state = 'PLAYING'
                self.shuffle_grid()
                self.start_time = time.time()
                return

        # Game Logic
        if self.state == 'PLAYING' and mx < VIDEO_SIZE:
            col = mx // TILE_SIZE
            row = my // TILE_SIZE
            index = row * GRID_SIZE + col
            
            # Start Drag
            if is_click_start:
                if 0 <= index < 16:
                    self.dragging = True
                    self.selected_tile = index
                    self.mouse_offset = (mx - col * TILE_SIZE, my - row * TILE_SIZE)

            # Drop / Swap
            elif is_click_release and self.dragging:
                # Target
                t_col = mx // TILE_SIZE
                t_row = my // TILE_SIZE
                t_index = t_row * GRID_SIZE + t_col
                
                # Perform Swap
                if 0 <= t_index < 16 and self.selected_tile is not None:
                    self.current_order[self.selected_tile], self.current_order[t_index] = \
                    self.current_order[t_index], self.current_order[self.selected_tile]
                    
                    if self.current_order == self.correct_order:
                        self.state = 'WON'
                
                self.dragging = False
                self.selected_tile = None

    def run(self):
        running = True
        while running:
            # 1. Capture Data
            frame_rgb, hand_pos, is_pinching = self.get_live_frame_and_hands()
            if frame_rgb is None: break
            
            full_surf = pygame.surfarray.make_surface(frame_rgb)
            self.hand_cursor_pos = hand_pos # Update global state

            # 2. Prepare Input Flags
            # Mouse Flags
            m_click_start = False
            m_click_release = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                elif event.type == pygame.MOUSEBUTTONDOWN: m_click_start = True
                elif event.type == pygame.MOUSEBUTTONUP: m_click_release = True
            
            # Hand Flags
            h_click_start = False
            h_click_release = False
            if hand_pos:
                if is_pinching and not self.was_pinching: h_click_start = True
                elif not is_pinching and self.was_pinching: h_click_release = True
                self.was_pinching = is_pinching

            # 3. Execute Logic (Mouse OR Hand)
            mx, my = pygame.mouse.get_pos()
            
            # Priority: Mouse Click -> Hand -> Mouse Move
            if m_click_start or m_click_release or (pygame.mouse.get_pressed()[0]):
                self.handle_input_logic((mx, my), m_click_start, m_click_release, True)
                current_cursor = (mx, my)
            elif hand_pos:
                self.handle_input_logic(hand_pos, h_click_start, h_click_release, is_pinching)
                current_cursor = hand_pos
            else:
                current_cursor = (mx, my)

            # 4. Update Time
            if self.state == 'PLAYING':
                self.elapsed_time = time.time() - self.start_time

            # 5. Drawing
            self.screen.fill((0,0,0))
            
            # Draw Game Grid
            if self.state == 'MENU':
                self.screen.blit(full_surf, (0,0))
                s = pygame.Surface((VIDEO_SIZE, VIDEO_SIZE))
                s.set_alpha(100); s.fill((0,0,0))
                self.screen.blit(s, (0,0))
            else:
                for i in range(16):
                    if self.dragging and i == self.selected_tile: continue
                    dx, dy = (i % GRID_SIZE) * TILE_SIZE, (i // GRID_SIZE) * TILE_SIZE
                    val = self.current_order[i]
                    sx, sy = (val % GRID_SIZE) * TILE_SIZE, (val // GRID_SIZE) * TILE_SIZE
                    self.screen.blit(full_surf, (dx, dy), (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, COLOR_GRID_LINES, (dx, dy, TILE_SIZE, TILE_SIZE), 1)

            # Draw Dragged Piece
            if self.dragging and self.selected_tile is not None:
                # Use current cursor position (Mouse or Hand)
                cx, cy = current_cursor
                val = self.current_order[self.selected_tile]
                sx, sy = (val % GRID_SIZE) * TILE_SIZE, (val // GRID_SIZE) * TILE_SIZE
                self.screen.blit(full_surf, (cx - self.mouse_offset[0], cy - self.mouse_offset[1]), (sx, sy, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.screen, COLOR_ACCENT, (cx - self.mouse_offset[0], cy - self.mouse_offset[1], TILE_SIZE, TILE_SIZE), 3)

            # Draw Sidebar
            self.draw_sidebar()

            # --- HAND CURSOR VISUALS ---
            if hand_pos:
                hx, hy = hand_pos
                # Draw a target reticle on the hand
                color = COLOR_SUCCESS if is_pinching else COLOR_HAND_CURSOR
                pygame.draw.circle(self.screen, color, (hx, hy), 10, 2)
                pygame.draw.circle(self.screen, color, (hx, hy), 4)
                if is_pinching:
                    pygame.draw.circle(self.screen, color, (hx, hy), 20, 1)

            # Win/Loss Overlays
            if self.state == 'WON':
                pygame.draw.rect(self.screen, COLOR_SUCCESS, (0, 0, VIDEO_SIZE, VIDEO_SIZE), 5)
                msg = self.font_big.render("ACCESS GRANTED", True, COLOR_SUCCESS)
                self.screen.blit(msg, (VIDEO_SIZE//2 - msg.get_width()//2, VIDEO_SIZE//2))
            elif self.state == 'LOST':
                pygame.draw.rect(self.screen, COLOR_FAIL, (0, 0, VIDEO_SIZE, VIDEO_SIZE), 5)
                msg = self.font_big.render("ACCESS DENIED", True, COLOR_FAIL)
                self.screen.blit(msg, (VIDEO_SIZE//2 - msg.get_width()//2, VIDEO_SIZE//2))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.cap.release()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = LiveJigsawCaptcha()
    game.run()