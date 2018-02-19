sudo pip3 uninstall neutronics_material_maker
sudo pip uninstall neutronics_material_maker

sudo python setup.py install --record files.txt
#cat files.txt | xargs rm -rf

sudo rm /usr/local/lib/python2.7/dist-packages/neutronics_material_maker-0.12-py2.7.egg