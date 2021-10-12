try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Need to fix the installation")
    raise


class Viewer:
    def __init__(self, frame_ind):
        self.frame_ind = frame_ind + 1

    def visualize1(self, curr_img, candidates_traffic_light_points):
        fig, curr_sec = plt.subplots(1, 1, figsize=(12, 6))
        curr_sec.set_title('curr(' + str(self.frame_ind) + ')')
        curr_sec.imshow(np.array(curr_img))
        curr_sec.plot(candidates_traffic_light_points[:, 0], candidates_traffic_light_points[:, 1], 'r.')
        # plt.show()

    def visualize2(self, curr_img, traffic_light_points):
        fig, curr_sec = plt.subplots(1, 1, figsize=(12, 6))
        curr_sec.set_title('curr(' + str(self.frame_ind) + ')')
        curr_sec.imshow(np.array(curr_img))
        curr_sec.plot(traffic_light_points[:, 0], traffic_light_points[:, 1], 'r.')
        # plt.show()

    def visualize3(self, curr_img, traffic_light_points, traffic_light_colors, valid, traffic_lights_3d_location):
        fig, curr_sec = plt.subplots(1, 1, figsize=(12, 6))
        curr_sec.set_title('curr(' + str(self.frame_ind) + ')')
        curr_sec.imshow(curr_img)
        # show points
        red_tfl = np.array(
            [traffic_light_points[i] for i in range(len(traffic_light_points)) if traffic_light_colors[i] == "red"])
        curr_sec.plot(red_tfl[:, 0], red_tfl[:, 1], 'r.')  # vis2
        green_tfl = np.array(
            [traffic_light_points[i] for i in range(len(traffic_light_points)) if traffic_light_colors[i] == "green"])
        curr_sec.plot(green_tfl[:, 0], green_tfl[:, 1], 'g.')  # vis2
        # show distances
        for i in range(len(traffic_light_points)):
            if valid[i]:
                curr_sec.text(traffic_light_points[i, 0], traffic_light_points[i, 1],
                              r'{0:.1f}'.format(traffic_lights_3d_location[i, 2]), color='y')
        plt.show()
        self.frame_ind += 1
