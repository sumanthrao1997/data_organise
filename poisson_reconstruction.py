import open3d as o3d
import os
rootdir = f'/automount_home_students/snagulavancha/Desktop/daml_data'
for subdir, _, files in os.walk(rootdir):
    if "laser" in subdir and "old" not in subdir: 
        for file in files:
            if "fruit.ply" in file:
                fruit_path = os.path.join(subdir, file)
            # if "old/" not in fruit_path:
                print(fruit_path)
                pcd = o3d.io.read_point_cloud(fruit_path)
                print('run Poisson surface reconstruction')
                mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
                print(mesh)
                mesh_path = os.path.join(subdir, "mesh.ply")
                print(mesh_path)
                o3d.visualization.draw_geometries([mesh])
                o3d.io.write_triangle_mesh(filename= mesh_path, mesh=mesh)
