from os import mkdir
import sys
import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation as R
from pathlib import Path
import argparse
import shutil
from tqdm import tqdm
def gen_random_rot_mat():
    rand_matrix = np.random.randint(0,360,(1,3))
    return R.from_euler('zyx', rand_matrix, degrees=True)

def apply_rot_pcl(filename, rotation_matrix, display=False):
    """
    returns : rotated numpy array
    """
    pcd = o3d.io.read_point_cloud(filename)
    pcl = np.asarray(pcd.points)
    # rotaion
    rpcl = rotation_matrix.apply(pcl)
    if(display):
        rot_pcd = o3d.geometry.PointCloud()
        rot_pcd.points = o3d.utility.Vector3dVector(rpcl)
        o3d.visualization.draw_geometries([pcd],window_name=filename)
        o3d.visualization.draw_geometries([rot_pcd],window_name="Roated point cloud")
    return rpcl

def apply_rot_npz(filename, rotaion_matrix, display=False):
    # reading and rotating npz files
    """
    return: two numpy arrays, pos and neg of shape (n,4)
    """
    # data = np.load("./p1/laser/samples.npz")
    data = np.load(filename)
    lst = data.files
    temp_list = []
    for item in lst:
        temp_list.append(data[item])
    pos = np.asarray(temp_list[0])
    neg = np.asarray(temp_list[1])
    rpos = np.hstack((rotaion_matrix.apply(pos[:,:-1]),pos[:,-1].reshape((len(pos),1))))
    rneg = np.hstack((rotaion_matrix.apply(neg[:,:-1]),neg[:,-1].reshape((len(pos),1))))
    # rpos = r.apply(pos[:,:-1])
    # rneg = r.apply(neg[:,:-1])
    if(display):
        rot_pos = o3d.geometry.PointCloud()
        rot_pos.points = o3d.utility.Vector3dVector(rpos[:,:-1])
        o3d.visualization.draw_geometries([rot_pos],window_name="Rotated Pos")
        rot_neg = o3d.geometry.PointCloud()
        rot_neg.points = o3d.utility.Vector3dVector(rneg[:,:-1])
        o3d.visualization.draw_geometries([rot_neg], window_name="Rotated neg")
    return pos, neg

def save_pcl(filename, pcl):
    pointcloud = o3d.geometry.PointCloud()
    pointcloud.points = o3d.utility.Vector3dVector(pcl)
    o3d.io.write_point_cloud(filename, pointcloud, print_progress=False)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=str,help="directpory where data is located")
    parser.add_argument("dest_path", type=str, help="directory where the rotated files should be stored")
    args =parser.parse_args()
    data_path = Path(args.data_path)
    dest_path = Path(args.dest_path)
    if(not data_path.exists()):
        print("data directory dosent exsist")
        sys.exit()
    if(not dest_path.exists()):
        dest_path.mkdir()
    # bar = progressbar.ProgressBar(maxval=len(members)).start()z

    for p in data_path.iterdir():
        ply = p/"laser"/"fruit.ply"
        npz = p/"laser"/"samples.npz"
        if ply.exists() and npz.exists():
            dest_dir = dest_path/p.name
            if(not (dest_dir/"0"/"laser").exists()): (dest_dir/"0"/"laser").mkdir(parents=True)
            dest_ply = dest_dir/"0"/"laser"/"fruit.ply"
            dest_ply.touch()
            shutil.copy(ply,dest_ply)
            dest_npz = dest_dir/"0"/"laser"/"samples.npz"
            dest_npz.touch()
            shutil.copy(npz,dest_npz)
            # copy file from src to destination
            # if (not dest_dir.exists()): dest_dir.mkdir(parents=True)
            for i in tqdm(range(1,11)):
                rot = gen_random_rot_mat()
                rpcl = apply_rot_pcl(str(ply), rot, display=False)
                pos,neg = apply_rot_npz(str(npz), rot, display=False)
                # saving it to destinati"on
                if(not (dest_dir/str(i)/"laser").exists()):(dest_dir/str(i)/"laser").mkdir(parents=True)
                dest_ply = dest_dir/str(i)/"laser"/"fruit.ply"
                dest_ply.touch()
                save_pcl(str(dest_ply),rpcl)
                dest_npz = dest_dir/str(i)/"laser"/"samples.npz"
                dest_npz.touch()
                np.savez_compressed(str(dest_npz),pos=pos,neg=neg)
                dest_rot = dest_dir/str(i)/"laser"/"rotation.csv"
                dest_rot.touch()
                np.savetxt(str(dest_rot), rot.as_matrix()[0], delimiter=",")


            
    # pcl_file = "./p1/laser/fruit.ply"
    # npz_file = "./p1/laser/samples.npz"

    
    # # saving pcl
    # p = Path(pcl_file)
    # z = Path(npz_file)
    # new_file = str(p.parent)+ "/" + p.stem+ str(1)+ p.suffix
    # # save_pcl(new_file,rpcl)
    # # saving rotation matrix
    # rot_file = str(p.parent)+ "/" + "rotation"+ str(1)+ ".csv"
    # # np.savetxt(rot_file,rot.as_matrix()[0],delimiter=",")
    # # saving as npz files
    # new_npz = str(z.parent)+ "/" + z.stem+ str(1)+ z.suffix
    # # np.savez_compressed(new_npz,pos=pos,neg=neg)
