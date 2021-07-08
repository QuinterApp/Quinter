cd "/users/Mason/Dropbox/avoid random evil guy/quinter"
rm -R macdist
pyinstaller --noupx --clean --windowed --osx-bundle-identifier me.masonasons.quinter quinter.pyw --noconfirm --distpath m1dist --workpath m1build
cp keymac.keymap m1dist/quinter.app/contents/resources/keymac.keymap
cp -R ../m1files/ m1dist/quinter.app/contents/resources
cp -R sounds m1dist/quinter.app
cp -R docs/ m1dist/
rm -R m1build
rm -R m1dist/quinter
rm -R /applications/Quinter.app
cp -R m1dist/quinter.app /applications/
zip -r -X m1dist/QuinterM1.zip m1dist
rm -R m1dist/quinter.app