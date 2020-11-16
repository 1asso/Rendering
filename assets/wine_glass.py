import bpy
import random
import os

for c in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.unlink(c)
    
obj_dir = '/Users/Ryan/Documents/Research/rendering/assets/obj/'
obj_files = os.listdir(obj_dir)
counts = [int(x.split('.')[0]) for x in obj_files if os.path.splitext(x)[1] == '.obj']
counts.append(0)

obj_count = max(counts) + 1

for i in range(obj_count, 100):
    
    objs = bpy.data.objects
    if 'wine-glass' in objs:
        objs.remove(objs['wine-glass'], do_unlink=True)
    
    verts = [[0, 0, 0], ]
    vert = verts[-1].copy()
    vert[0] -= random.uniform(0.8, 1.5)
    verts.append(vert)

    vert = verts[-1].copy()
    vert[2] += random.uniform(0.1, 0.2)
    verts.append(vert)

    for i in range(9):
        vert = verts[-1].copy()
        vert[0] -= random.uniform(vert[0] / 5, vert[0] / 3)
        vert[2] += random.uniform(0.02, 0.06)
        verts.append(vert)
        
    vert = verts[-1].copy()
    vert[2] += random.uniform(1.5, 2.5)
    verts.append(vert)


    choice = random.randint(0, 2)

    if choice == 0:
        tmp_x = 0.1 * verts[1][0]
        for i in range(1, 23):
            vert = verts[-1].copy()
            vert[0] += random.uniform(0.04 * tmp_x * (24-i), 0.06 * tmp_x * (24-i))
            vert[2] += random.uniform(0.01 * i, 0.02 * i)
            verts.append(vert)

    if choice == 1:
        tmp_x = 0.1 * verts[1][0]
        for i in range(1, 17):
            vert = verts[-1].copy()
            vert[0] += random.uniform(0.08 * tmp_x * (17-i), 0.12 * tmp_x * (17-i))
            vert[2] += random.uniform(0.008 * i, 0.015 * i)
            verts.append(vert)
        
        tmp_y = verts[-1][2] - verts[-2][2]
        for i in range(-4, 4):
            vert = verts[-1].copy()
            vert[0] -= random.uniform(0.1 * tmp_x * (5- abs(i)), 0.15 * tmp_x * (5- abs(i)))
            vert[2] += tmp_y
            verts.append(vert)
            
    if choice == 2:
        tmp_x = 0.1 * verts[1][0]
        for i in range(1, 13):
            vert = verts[-1].copy()
            vert[0] += random.uniform(0.13 * tmp_x * (14-i), 0.17 * tmp_x * (14-i))
            vert[2] += random.uniform(0.005 * i, 0.01 * i)
            verts.append(vert)
        
        tmp_y = verts[-1][2] - verts[-2][2]
        for i in range(-4, 4):
            vert = verts[-1].copy()
            vert[0] -= random.uniform(0.13 * tmp_x * (5- abs(i)), 0.25 * tmp_x * (5- abs(i)))
            vert[2] += tmp_y
            verts.append(vert)
            
        for i in range(1, 9):
            vert = verts[-1].copy()
            vert[0] -= random.uniform(0.015 * tmp_x * (10-i), 0.03 * tmp_x * (10-i))
            vert[2] += 2 * tmp_y / 3
            verts.append(vert)

    num_verts = len(verts)
    for i in range(num_verts-1, 13, -1):
    #    print(i)
        vert = verts[i]
        verts.append((vert[0]+0.1, 0, vert[2]))
    verts.append((0, 0, verts[14][2]))
        
    print(len(verts))

    mymesh = bpy.data.meshes.new("wine-glass")
    myobject = bpy.data.objects.new("wine-glass", mymesh)  

     
    #Set location and scene of object
    myobject.location = bpy.context.scene.cursor.location
    bpy.context.collection.objects.link(myobject)

    #Create mesh
    mymesh.from_pydata(verts,[],[])
    mymesh.update(calc_edges=True)

    bpy.context.view_layer.objects.active = myobject

    verts = myobject.data.vertices
    for i in range(len(verts)-1):
    #    print(verts[i].co)
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action='DESELECT')
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        verts[i].select = True
        verts[i+1].select = True
        
        bpy.ops.object.mode_set(mode = 'EDIT') 

        bpy.ops.mesh.edge_face_add()



    bpy.ops.object.modifier_add(type='SCREW')
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Screw"].use_normal_flip = True

    target_file = os.path.join(obj_dir, f'{obj_count}.obj')

    bpy.ops.export_scene.obj(filepath=target_file, use_materials=False)
    
    obj_count += 1