cd "/users/Mason/Dropbox/projects/python/py3/quinter"
rm -R macdist
pyinstaller --noupx --clean --windowed --osx-bundle-identifier me.masonasons.quinter quinter.pyw --noconfirm --distpath macdist --workpath macbuild
cp keymac.keymap dist/quinter.app/contents/resources/keymac.keymap
cp -R ../macfiles/ macdist/quinter.app/contents/resources
cp -R sounds macdist/quinter.app
cp -R docs/ macdist/
rm -R macbuild
rm -R macdist/quinter
rm -R /applications/Quinter.app
cp -R macdist/quinter.app /applications/
zip -r -X macdist/QuinterMac.zip macdist
rm -R macdist/quinter.app