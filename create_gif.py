import os
from os.path import join
import glob
import numpy as np
import open3d as o3d
import imageio
from PIL import Image
import argparse

def capture_pcd(ply_path, save_dir):
    pcd = o3d.io.read_point_cloud(ply_path)
    
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible = False)
    vis.add_geometry(pcd)
    # vis.get_render_option().mesh_show_back_face = True
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    ctr = vis.get_view_control()

    # change the view directions
    ctr.set_up((0, -1, 0))
    ctr.set_front((0, 0, -1))
    # ctr.set_front((0, 0, 1))
    # ctr.change_field_of_view(0.3)
    ctr.change_field_of_view(3.0)
    vis.poll_events()
    vis.update_renderer()

    for i in range(30):
        if i == 0:
            ctr.rotate(300.0, 0.0)
        else:
            ctr.rotate(-20.0, 0.0)
        vis.poll_events()
        vis.update_renderer()
        vis.capture_screen_image(join(save_dir, f'view_{i:03}.png'))

def capture_mesh(ply_path, save_dir):
    mesh = o3d.io.read_triangle_mesh(ply_path)
    
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible = False)
    vis.add_geometry(mesh)
    vis.get_render_option().mesh_show_back_face = True
    vis.update_geometry(mesh)
    vis.poll_events()
    vis.update_renderer()
    ctr = vis.get_view_control()

    # change the view directions
    '''
    ctr.set_up((0, -1, 0))
    ctr.set_front((0, 0, -1))
    ctr.set_front((0, 0, 1))
    '''
    ctr.change_field_of_view(3.0)
    vis.poll_events()
    vis.update_renderer()

    for i in range(30):
        if i == 0:
            ctr.rotate(300.0, 0.0)
        else:
            ctr.rotate(-20.0, 0.0)
        vis.poll_events()
        vis.update_renderer()
        vis.capture_screen_image(join(save_dir, f'view_{i:03}.png'))


def make_gif(img_dir):
    img_paths = glob.glob(join(img_dir, '*.png'))
    img_paths.sort()
    img_list = []

    for img_path in img_paths:
        image = np.asarray(Image.open(img_path))
        image = (image / 255).astype(np.float32)
        img_list.append(image)

    stacked_imgs = [to8b(np_img) for np_img in img_list]
    file_name = f'video.gif'

    os.makedirs(join(img_dir, 'vids'), exist_ok=True)
    imageio.mimwrite(join(img_dir, 'vids', file_name), stacked_imgs, fps=7, format='GIF')
    print("### finished generating gif ###")

def to8b(x):
    return (255 * np.clip(x, 0, 1)).astype(np.uint8)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ply_path', help='directory of input .ply files')
    parser.add_argument('--type', help='specify mesh or point cloud')
    parser.add_argument('--save_dir', help='path to save the gif file')
    args = parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)

    # (1) Capture the geometry from different viewpoints
    if args.type == 'mesh':
        capture_mesh(
            args.ply_path,
            args.save_dir
        )
    elif args.type == 'pcd':
        capture_pcd(
            args.ply_path,
            args.save_dir
        )
    else:
        raise Exception("wrong type: only mesh and point cloud is available!")

    # (2) Make the gif from the captured images.
    make_gif(args.save_dir)

if __name__=='__main__':
    main()