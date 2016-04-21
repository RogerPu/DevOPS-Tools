pvcreate /dev/sdb1
vgextend VolGroup /dev/sdb1
lvextend -L +19.99GB -n /dev/VolGroup/lv_root
resize2fs /dev/VolGroup/lv_root
