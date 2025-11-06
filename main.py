import sys
import re
import math
from collections import deque

sys.setrecursionlimit(200000)

def solve_accuracy_focused_dog():
    """
    راه‌حل نهایی با تمرکز کامل بر روی دقت، با استفاده از پایپ‌لاین هیبریدی.
    """
    try:
        lines = sys.stdin.readlines()
        if not lines: return
        h, w, expected = map(int, lines[0].strip().split())

        intensity_map = [[0.0 for _ in range(w)] for _ in range(h)]
        for r in range(h):
            numbers = list(map(int, re.findall(r'\d+', lines[r+1])))
            for c in range(w):
                idx = c * 3
                r_val, g_val, b_val = numbers[idx], numbers[idx+1], numbers[idx+2]
                intensity_map[r][c] = (r_val + g_val + b_val) / 3.0

    except (IOError, ValueError):
        return

    def gaussian_blur(image, sigma):
        # پیاده‌سازی دقیق اما کند برای حداکثر دقت
        size = int(2 * 4 * sigma + 1)
        if size % 2 == 0: size += 1
        kernel = [math.exp(-x**2 / (2 * sigma**2)) for x in range(-size//2, size//2 + 1)]
        kernel_sum = sum(kernel)
        kernel = [k / kernel_sum for k in kernel]
        
        blurred_h = [[0.0 for _ in range(w)] for _ in range(h)]
        for r in range(h):
            for c in range(w):
                val = 0.0
                for i in range(size):
                    offset = i - size//2
                    if 0 <= c + offset < w:
                        val += image[r][c + offset] * kernel[i]
                blurred_h[r][c] = val
        
        blurred_v = [[0.0 for _ in range(w)] for _ in range(h)]
        for r in range(h):
            for c in range(w):
                val = 0.0
                for i in range(size):
                    offset = i - size//2
                    if 0 <= r + offset < h:
                        val += blurred_h[r + offset][c] * kernel[i]
                blurred_v[r][c] = val
        return blurred_v

    # --- مرحله 1: تشخیص کاندیداها با DoG ---
    blur1 = gaussian_blur(intensity_map, 2.5)
    blur2 = gaussian_blur(intensity_map, 4.0)
    
    dog_image = [[blur1[r][c] - blur2[r][c] for c in range(w)] for r in range(h)]

    peaks = []
    MIN_PEAK_VALUE = 2.0
    for r in range(1, h-1):
        for c in range(1, w-1):
            val = dog_image[r][c]
            if val > MIN_PEAK_VALUE:
                is_max = all(val > dog_image[r+dr][c+dc] for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0))
                if is_max:
                    peaks.append({'dog_score': val, 'center': (r, c)})

    # --- مرحله 2: امتیازدهی هوشمند و ترکیبی ---
    all_candidates = []
    WINDOW_SIZE = 7
    half_window = WINDOW_SIZE // 2

    for peak in peaks:
        r_center, c_center = peak['center']
        intensity_score = 0
        for dr in range(-half_window, half_window + 1):
            for dc in range(-half_window, half_window + 1):
                nr, nc = r_center + dr, c_center + dc
                if 0 <= nr < h and 0 <= nc < w:
                    intensity_score += intensity_map[nr][nc]
        
        # محاسبه امتیاز نهایی
        final_score = peak['dog_score'] * intensity_score
        all_candidates.append({
            'score': final_score, 
            'center': (r_center, c_center)
        })

    # --- مرحله نهایی: مرتب‌سازی و فیلتر کردن ---
    all_candidates.sort(key=lambda s: s['score'], reverse=True)
    
    final_stars = []
    MIN_DISTANCE_SQ = 10**2
    
    for star in all_candidates:
        is_far_enough = True
        r1, c1 = star['center']
        for final_star in final_stars:
            r2, c2 = final_star['center']
            dist_sq = (r1 - r2)**2 + (c1 - c2)**2
            if dist_sq < MIN_DISTANCE_SQ:
                is_far_enough = False
                break
        if is_far_enough:
            final_stars.append(star)

    num_to_output = min(expected, len(final_stars))
    
    print(num_to_output)
    for i in range(num_to_output):
        r_center, c_center = final_stars[i]['center']
        print("{} {}".format(r_center + 1, c_center + 1))

solve_accuracy_focused_dog()