try:
    import numpy as np
    from PIL import Image
    from tfl_manager import TFL_manager
    from viewer import Viewer
except ImportError:
    print("Need to fix the installation")
    raise


class Controller:
    def __init__(self):
        pass

    def get_tfl_data(self, play_list):
        images = []
        with open(play_list, 'r') as fp:
            pkl_f = fp.readline()
            frame_ind = int(fp.readline()[:-1])
            while True:
                image = fp.readline()
                if image == '':
                    break
                images.append(image[:-1])
        return pkl_f[:-1], frame_ind, images

    def tfl_controller(self, play_list):
        pkl_f, frame_ind, images = self.get_tfl_data(play_list)
        tfl_manager = TFL_manager(pkl_f)
        viewer = Viewer(frame_ind)
        for i in range(len(images)):
            tfl_positions, tfl_colors, valid, tfl_distance = tfl_manager.calculate_tfl_distance(images[i],
                                                                                                frame_ind + i)
            if tfl_distance is not None:
                viewer.visualize3(np.array(Image.open(images[i])), np.array(tfl_positions), np.array(tfl_colors), valid,
                                  tfl_distance)
