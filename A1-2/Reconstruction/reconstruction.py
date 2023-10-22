import numpy as np
import cv2
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import lsqr

if __name__ == '__main__':
    # Read the source image
    img_path = 'large1.jpg'
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Calculate the Laplacian for the source image
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    
    # Height and width of the image
    h, w = img.shape

    # Initialize the coefficient matrix A and known right-hand side vector b (Laplacian)
    A = lil_matrix((h * w, h * w))  # using sparse matrix representation
    b = np.zeros(h * w)

    # Set up the matrix equation Av = b
    for y in range(1, h-1):
        for x in range(1, w-1):
            idx = y * w + x
            A[idx, idx] = 4
            A[idx, idx - 1] = -1
            A[idx, idx + 1] = -1
            A[idx, idx - w] = -1
            A[idx, idx + w] = -1
            b[idx] = laplacian[y, x]

    # Imposing the constraints for the four corners
    corner_indices = [0, w-1, (h-1)*w, h*w-1]
    A[corner_indices, :] = 0
    for idx in corner_indices:
        A[idx, idx] = 1
    b[corner_indices] = [1, 2, 3, 4]

    # Solve for v using optimized solver for sparse matrices
    v, _ = lsqr(A, b)[:2]
    
    # Compute the least square error
    error = np.linalg.norm(A @ v - b)
    print("the least square error is:", error)

    # Reshape v to the shape of the target image
    reconstructed_image = v.reshape(h, w)

    cv2.imwrite('reconstructed_large1.jpg', reconstructed_image)