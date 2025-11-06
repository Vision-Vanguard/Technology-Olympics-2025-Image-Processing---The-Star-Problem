✨ Star/Point-of-Interest Detection Using Difference of Gaussians (DoG)

This repository contains a Python solution for a point-of-interest detection problem, likely from Quera (Problem ID: 14442), which involves identifying and localizing a specific number of features (like stars in an astronomical image) within a given image map.

🌟 The Problem: Identifying Stars (Inferred)

The problem likely requires reading an image map (represented by a grid of RGB values) and a target number of features, K (referred to as expected in the code). The goal is to:

    Process the Image: Convert the color image data into a single-channel intensity map.

    Detect Candidates: Use an image processing technique to identify locations that are significantly brighter or distinct from their immediate surroundings, representing potential stars.

    Score and Rank: Assign a comprehensive score to each candidate location.

    Filter and Output: Select the top K features, ensuring they are not too close to each other (non-maximum suppression), and output their 1-based coordinates.

💡 The Solution: Hybrid DoG and Intensity Scoring

The provided solution, solve_accuracy_focused_dog, utilizes a hybrid approach to maximize accuracy, combining the robust detection power of the Difference of Gaussians (DoG) with local intensity-based scoring.

1. Image Preprocessing

    Intensity Calculation: The input R,G,B values for each pixel are converted into a single floating-point intensity value by averaging the three color components:
    Intensity=(R+G+B)/3.0

2. Difference of Gaussians (DoG) for Candidate Detection

The core detection mechanism is the DoG, which is an efficient approximation of the Laplacian of Gaussian (LoG), a fundamental technique in feature detection (like in the SIFT algorithm).

    Gaussian Blurring: The intensity map is blurred twice with two different σ (standard deviation) values:

        Blur1​: σ=2.5 (finer details)

        Blur2​: σ=4.0 (broader context)

        Note: The code includes a custom, though potentially slow, high-accuracy implementation of the 1D Gaussian filter applied separately in the horizontal and vertical directions.

    DoG Image: The difference between the two blurred images highlights areas where the intensity changes rapidly and abruptly, which are strong indicators of point features (stars):
    DoG=Blur1​−Blur2​

    Peak Identification: The code then searches the dog_image for local maxima whose value exceeds a threshold (MIN_PEAK_VALUE = 2.0). These strong local maxima form the set of initial candidates (peaks).

3. Smart and Combined Scoring

To refine the candidates found by the DoG, a second scoring mechanism is introduced, which accounts for the actual brightness of the feature:

    Local Intensity Sum: For each DoG peak, the surrounding pixels within a small window (WINDOW_SIZE = 7) in the original intensity map are summed up to calculate an intensity_score. This ensures the candidate is not just a strong DoG response but also a genuinely bright spot.

    Final Score: The ultimate score for ranking candidates is a multiplication of the two component scores:
    Final Score=DoG Score×Intensity Score

4. Final Filtering and Output

    Ranking: All candidates are sorted in descending order based on their Final Score.

    Non-Maximum Suppression (NMS): This is a crucial step to prevent detecting the same star multiple times or selecting stars that are too close to each other.

        The code iterates through the ranked candidates and adds a star to the final list (final_stars) only if its distance squared from all previously selected stars is greater than a minimum threshold (`MIN_DISTANCE_SQ = 10^2$, or a distance of 10 pixels).

    Output: The final number of detected stars is min(expected,len(final_stars)), and their 1-based coordinates are printed.

📉 Score Analysis (75%)

Achieving 75% suggests that the core logic is sound, but there might be edge cases or precision issues preventing a perfect score:

    Gaussian Blur Precision: The custom Gaussian implementation, while accuracy-focused, might still introduce minor rounding differences compared to an optimized library (like NumPy or OpenCV), especially for floating-point arithmetic.

    Parameter Tuning: The choice of parameters (σ values: 2.5 and 4.0, MIN_PEAK_VALUE = 2.0, WINDOW_SIZE = 7, `MIN_DISTANCE_SQ = 100$) is critical. Optimizing these thresholds and window sizes based on the specific characteristics of the test cases could potentially increase the score.

    Boundary Cases: Handling of image boundaries within the gaussian_blur and peak detection loops is essential and a common area for minor errors. The current code correctly checks bounds (0 <= c + offset < w, etc.).
