import os
import numpy as np
import cv2
import dlib

BIOID_IMAGE_FOLDER = 'G:/Datasets/BioID/Images/'

FACE_DETECTOR = dlib.get_frontal_face_detector()

PREDICTOR_PATH = 'shape_predictor_68_face_landmarks.dat'
PREDICTOR = dlib.shape_predictor(PREDICTOR_PATH)

BLUE = (255, 0, 0)
RED = (0, 0, 255)

def get_facial_points(img):
    # find face in image
    dets = FACE_DETECTOR(img)
    face_rect_dlib = det_to_rect(dets[0])
    face_rect_dlib = resize_rect(face_rect_dlib, [1.5, 1.5])

    # find facial feature points
    shape = PREDICTOR(img, dets[0])
    points = []
    for s in range(shape.num_parts):
        point = [shape.part(s).x, shape.part(s).y]
        points.append(point)
    return points

def det_to_rect(d):
    x1 = d.left()
    x2 = d.right()
    y1 = d.top()
    y2 = d.bottom()
    face_rect = [x1, y1, x2-x1, y2-y1]
    return face_rect

def get_sub_image(img, rect):
    # sub = img[y1:y2, x1:x2]
    sub = img[rect[1]:(rect[1]+rect[3]),
              rect[0]:(rect[0]+rect[2])]
    return sub

def resize_rect(rect, scale):
    diff_w = rect[2] - rect[2]*scale[0]
    diff_h = rect[3] - rect[3]*scale[1]
    new_rect = [int(rect[0]+diff_w/2),
                int(rect[1]+diff_h/2),
                int(rect[2]*scale[0]),
                int(rect[3]*scale[1])]
    return new_rect

def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True

def add_border_points(points, rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    points.append([x, y])
    points.append([x, y+(h/2)-1])
    points.append([x, y+h-1])
    points.append([x+(w/2)-1, y])
    points.append([x+w-1, y])
    points.append([x+w-1, y+(h/2)-1])
    points.append([x+(w/2)-1, y+h-1])
    points.append([x+w-1, y+h-1])
    return points

def get_local_coordinates(tri, rect):
    # Offset points by left top corner of rect
    local_tri = []
    for i in xrange(0, 3):
        lx = tri[i][0] - rect[0]
        ly = tri[i][1] - rect[1]
        local_tri.append((lx, ly))
    return local_tri

def prune_triangles(tri, img):
    pruned_tri = []
    size = img.shape
    rect = (0, 0, size[1], size[0])
    for t in tri:
        if rect_contains(rect, t[0]) and \
           rect_contains(rect, t[1]) and \
           rect_contains(rect, t[2]):
            pruned_tri.append(t)
    return pruned_tri

def get_triangle_indices(tri_list, points):
    idx_list = []
    for t in tri_list:
        tri_ind = [0, 0, 0]
        for idx, p in enumerate(points):
            if p[0] == t[0][0] and p[1] == t[0][1]:
                tri_ind[0] = idx
            if p[0] == t[1][0] and p[1] == t[1][1]:
                tri_ind[1] = idx
            if p[0] == t[2][0] and p[1] == t[2][1]:
                tri_ind[2] = idx
        idx_list.append(tri_ind)
    return idx_list

def convert_triangle_list(tri_list):
    new_list = []
    for t in tri_list:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        # create triangles defined as point lists
        tri = [pt1, pt2, pt3]
        new_list.append(tri)
    return new_list

def draw_triangle_list(img, window_name, points, tri_list):
    # debug drawing
    debug_img = img.copy()
    radius = 1
    for point in points:
        cv2.circle(debug_img, (int(point[0]), int(point[1])), radius, BLUE, -1)

    # show image
    thickness = 1
    for t in tri_list:
        cv2.line(debug_img, tuple(t[0]), tuple(t[1]), BLUE, thickness)
        cv2.line(debug_img, tuple(t[0]), tuple(t[2]), BLUE, thickness)
        cv2.line(debug_img, tuple(t[1]), tuple(t[2]), BLUE, thickness)

    cv2.namedWindow(window_name)
    cv2.imshow(window_name, debug_img)

def delauney_triangulation(img, points):
    # create delauney triangulation
    size = img.shape
    rect = (0, 0, size[1], size[0])
    subdiv = cv2.Subdiv2D(rect)
    subdiv.insert(points)
    tri_list = subdiv.getTriangleList()
    tri_list = convert_triangle_list(tri_list)
    tri_list = prune_triangles(tri_list, img)

    # find out which points indices that form triangles
    ind_list = get_triangle_indices(tri_list, points)
    return tri_list, ind_list

def create_matching_triangles(tri_ind, points):
    tri_list = []
    for ind in tri_ind:
        tri = [tuple(points[ind[0]]),
               tuple(points[ind[1]]),
               tuple(points[ind[2]])]
        tri_list.append(tri)
    return tri_list

def warp_image(img, ref_img, tri, ref_tri):
    warp_img = ref_img.copy()

    # check that both have the same number of triangles
    # assume same order
    if len(tri) == len(ref_tri):
        for i, tri1 in enumerate(tri):
            tri2 = ref_tri[i]

            # find bounding rects of triangles
            roi1 = cv2.boundingRect(np.float32(tri1))
            roi2 = cv2.boundingRect(np.float32(tri2))

            # calculate local triangle coordinates in sub image
            local_tri1 = get_local_coordinates(tri1, roi1)
            local_tri2 = get_local_coordinates(tri2, roi2)

            # get affine transform from tri1 to tri2 in local coordinates
            warp_map = cv2.getAffineTransform(np.float32(local_tri1), np.float32(local_tri2))

            # warp from sub image 1 to sub image 2
            sub1 = get_sub_image(img, roi1)
            warp_sub = cv2.warpAffine(np.float32(sub1), warp_map, \
                                      (roi2[2], roi2[3]), \
                                      None, flags=cv2.INTER_LINEAR, \
                                      borderMode=cv2.BORDER_REFLECT_101)

            # create a mask to remove pixels outside the triangle
            mask = np.zeros((roi2[3], roi2[2], 3), dtype=np.float32)
            cv2.fillConvexPoly(mask, np.int32(local_tri2), (1.0, 1.0, 1.0), 16)

            # Apply mask to cropped region
            warp_sub = np.uint8(warp_sub * mask)

            # Copy triangular region of the rectangular patch to the output image
            sub2 = get_sub_image(warp_img, roi2)
            sub2 = sub2 * ((1.0, 1.0, 1.0) - mask)
            warp_img[roi2[1]:roi2[1]+roi2[3], roi2[0]:roi2[0]+roi2[2]] = sub2 + warp_sub
    return warp_img

def main():
    # load images
    img1 = cv2.imread(os.path.join(BIOID_IMAGE_FOLDER, 'BioID_0001.pgm'))
    img2 = cv2.imread(os.path.join(BIOID_IMAGE_FOLDER, 'BioID_0019.pgm'))

    # extract facial points
    points1 = get_facial_points(img1)
    points2 = get_facial_points(img2)

    # perform delauney triangulation on first image and create the same set of triangles
    # with the other set of points. this assumes that the same number of points.
    tri1, tri_ind = delauney_triangulation(img1, points1)
    tri2 = create_matching_triangles(tri_ind, points2)

    # visualize triangles
    draw_triangle_list(img1, 'img1', points1, tri1)
    draw_triangle_list(img2, 'img2', points2, tri2)

    # perform a face warp
    warp_img = warp_image(img1, img2, tri1, tri2)
    cv2.namedWindow('warp')
    cv2.imshow('warp', warp_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
