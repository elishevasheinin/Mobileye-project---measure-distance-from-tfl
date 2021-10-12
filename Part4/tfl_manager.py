

try:
    import pickle
    from Part1 import find_tfl_candidates
    from Part2 import filter_tfl_points
    from Part3.SFM import calc_TFL_dist
except ImportError:
    print("Need to fix the installation")
    raise


class FrameContainer(object):
    def __init__(self, tfl_points, tfl_colors, EM=None):
        if EM is None:
            EM = []
        self.traffic_light_positions = tfl_points
        self.traffic_light_colors = tfl_colors
        self.traffic_lights_3d_location = []
        self.EM = EM
        self.corresponding_ind = []
        self.valid = []


class TFL_manager:
    def __init__(self, pkl_path):
        with open(pkl_path, 'rb') as pkl_file:
            self.__pkl_file = pickle.load(pkl_file, encoding='latin1')
        self.__prev_image_tfl = None
        self.__focal = self.__pkl_file['flx']
        self.__pp = self.__pkl_file['principle_point']
        self.__model = filter_tfl_points.Filter()

    def calculate_tfl_distance(self, curr_image, index):
        tfl_candidates, tfl_colors = self.find_suspicious_points(curr_image)
        EM = self.__pkl_file['egomotion_' + str(index - 1) + '-' + str(index)]
        frame_container = FrameContainer(tfl_candidates, tfl_colors, EM)
        frame_container.traffic_light_positions, frame_container.traffic_light_colors = self.filter_tfl_points(
            curr_image, frame_container.traffic_light_positions, frame_container.traffic_light_colors)
        if self.__prev_image_tfl == None:
            self.__prev_image_tfl = frame_container
            return None, None, None, None
        tfl_positions, valid, tfl_distance = self.calculate_distance(self.__prev_image_tfl, frame_container,
                                                                     self.__pp, self.__focal)
        self.__prev_image_tfl = frame_container
        return tfl_positions, tfl_colors, valid, tfl_distance

    def find_suspicious_points(self, curr_image):
        tfl_candidates, tfl_colors = find_tfl_candidates.find_tfl_lights(curr_image)
        return tfl_candidates, tfl_colors

    def filter_tfl_points(self, curr_image, candidates, colors):
        tfl_points, tfl_colors = self.__model.filter_points(curr_image, candidates, colors)
        return tfl_points, tfl_colors

    def calculate_distance(self, prev_tfl_container, curr_tfl_container, pp, focal_length):
        curr_tfl_container = calc_TFL_dist(prev_tfl_container, curr_tfl_container, pp, focal_length)
        return curr_tfl_container.traffic_light_positions, curr_tfl_container.valid, curr_tfl_container.traffic_lights_3d_location
