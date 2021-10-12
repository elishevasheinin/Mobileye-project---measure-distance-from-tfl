try:
    import numpy as np
except ImportError:
    print("Need to fix the installation")
    raise


def calc_TFL_dist(prev_container, curr_container, pp, focal):
    norm_prev_pts, norm_curr_pts, R, foe, tZ = prepare_3D_data(prev_container, curr_container, focal, pp)
    if (abs(tZ) < 10e-6):
        print('tz = ', tZ)
    elif (norm_prev_pts.size == 0):
        print('no prev points')
    elif (norm_prev_pts.size == 0):
        print('no curr points')
    else:
        curr_container.corresponding_ind, curr_container.traffic_lights_3d_location, curr_container.valid = calc_3D_data(
            norm_prev_pts, norm_curr_pts, R, foe, tZ, focal)
    return curr_container


def prepare_3D_data(prev_container, curr_container, focal, pp):
    norm_prev_pts = normalize(prev_container.traffic_light_positions, focal, pp)
    norm_curr_pts = normalize(curr_container.traffic_light_positions, focal, pp)
    R, foe, tZ = decompose(np.array(curr_container.EM))
    return norm_prev_pts, norm_curr_pts, R, foe, tZ


def calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ, focal):
    norm_rot_pts = rotate(norm_prev_pts, R)
    pts_3D = []
    corresponding_ind = []
    validVec = []
    for p_curr in norm_curr_pts:
        in_prev = False
        for point in unnormalize(norm_rot_pts, focal, foe):
            p = unnormalize(np.array([p_curr]), focal, foe)
            if point[0] > p[0, 0] - 40 and point[0] < p[0, 0] + 40 and point[1] > p[0, 1] - 40 and point[1] < p[
                0, 1] + 40:
                in_prev = True
        if not in_prev:
            validVec.append(False)
            continue
        corresponding_p_ind, corresponding_p_rot = find_corresponding_points(p_curr, norm_rot_pts, focal, foe)
        Z = calc_dist(p_curr, corresponding_p_rot, foe, tZ)
        valid = (Z > 0)
        if not valid:
            Z = 0
        validVec.append(valid)
        P = Z * np.array([p_curr[0], p_curr[1], 1])
        pts_3D.append((P[0], P[1], P[2]))
        corresponding_ind.append(corresponding_p_ind)
    return corresponding_ind, np.array(pts_3D), validVec


def normalize(pts, focal, pp):
    return np.array([np.array([(x[0] - pp[0]) / focal, (x[1] - pp[1]) / focal, 1]) for x in pts])


def unnormalize(pts, focal, pp):
    return np.array([(focal * x[0] + pp[0], focal * x[1] + pp[1]) for x in pts])


def decompose(EM):
    tx, ty, tz = EM[0, -1], EM[1, -1], EM[2, -1]
    R = EM[:-1, :-1]
    foe = (tx / tz, ty / tz)
    return R, foe, tz


def rotate(pts, R):
    return_array = []
    for x in pts:
        abc = np.dot(R, x)
        return_array.append([abc[0] / abc[2], abc[1] / abc[2]])
    return np.array(return_array)


def find_corresponding_points(p, norm_pts_rot, focal, foe):
    # compute the epipolar line between p and foe
    # run over all norm_pts_rot and find the one closest to the epipolar line
    # return the closest point and its index
    m = (foe[1] - p[1]) / (foe[0] - p[0])
    n = (p[1] * foe[0] - foe[1] * p[0]) / (foe[0] - p[0])
    points = [abs(x[1] - (m * x[0] + n)) for x in norm_pts_rot]
    return points.index(min(points)), norm_pts_rot[points.index(min(points))]


def calc_dist(p_curr, p_rot, foe, tZ):
    # calculate the distance of p_curr using x_curr, x_rot, foe_x and tZ
    # calculate the distance of p_curr using y_curr, y_rot, foe_y and tZ
    # combine the two estimations and return estimated Z
    return ((tZ * (foe[0] - p_rot[0])) / (p_curr[0] - p_rot[0]) + (tZ * (foe[1] - p_rot[1])) / (
            p_curr[1] - p_rot[1])) / 2
