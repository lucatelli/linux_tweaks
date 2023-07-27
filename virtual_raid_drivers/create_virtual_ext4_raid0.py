"""
Virtual RAID0 drive using HDDs to speed up things.
"""


import os
def return_counts(size,block_size=32000):
    return(size*(1.024e6)/block_size)

#the performance of CASA processing can be increased by a factor of 200-400% using
#a virtual raid0.
size1 = 150 * 1024 # 150GB virtual image
counts1 = return_counts(size1)
size2 = 150 * 1024 # 150GB virtual image
counts2 = return_counts(size2)
size3 = 150 * 1024 # 150GB virtual image
counts3 = return_counts(size3)



#image 1
# par_1_path = '/disk1/par1/folder1/'#do not touch disk, only folder1 inside it
par_1_path = '/run/media/sagauga/xfs_system/'
os.system('dd if=/dev/zero of='+par_1_path+'ext4_1.img status=progress bs=32k count='+str(int(counts1)))
os.system('mkfs.ext4 '+par_1_path+'ext4_1.img')
os.system('tune2fs -c0 -i0 '+par_1_path+'ext4_1.img')

#image 2
# par_2_path = '/disk1/par1/folder1/'#do not touch disk, only folder2 inside it
par_2_path = '/run/media/sagauga/storage_wd_2/'
os.system('dd if=/dev/zero of='+par_2_path+'ext4_2.img status=progress bs=32k count='+str(int(counts2)))
os.system('mkfs.ext4 '+par_2_path+'ext4_2.img')
os.system('tune2fs -c0 -i0 '+par_2_path+'ext4_2.img')

#image 3
# par_2_path = '/disk1/par1/folder1/'#do not touch disk, only folder2 inside it
par_3_path = '/run/media/sagauga/data/'
os.system('dd if=/dev/zero of='+par_3_path+'ext4_3.img status=progress bs=32k count='+str(int(counts3)))
os.system('mkfs.ext4 '+par_3_path+'ext4_3.img')
os.system('tune2fs -c0 -i0 '+par_3_path+'ext4_3.img')


'''
sudo losetup /dev/loop1 /run/media/sagauga/xfs_system/ext4_1.img
sudo losetup /dev/loop2 /run/media/sagauga/storage_wd_2/ext4_2.img
sudo losetup /dev/loop3 /run/media/sagauga/data/ext4_3.img

sudo mdadm --create /dev/md0 --level=0 --raid-devices=3 /dev/loop1 /dev/loop2 /dev/loop3
sudo mkfs.ext4 /dev/md0

sudo mkdir /run/media/sagauga/data_processing
sudo mount /dev/md0 /run/media/sagauga/data_processing/
sudo chown sagauga:sagauga /run/media/sagauga/data_processing/
sudo chown sagauga:sagauga /run/media/sagauga/data_processing/*

'''
