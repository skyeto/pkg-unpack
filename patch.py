import brotli
import re
import sys

FILENAME = sys.argv[1]
PATCHED_BYTES = 0
PREVENT_EXECUTION = True

src_fd = open(FILENAME, "rb")
src = bytearray(src_fd.read())
src_fd.close()

LEN = len(src)

patch__FILENAME = b"const z = Math.floor(Math.random()*100000);"

# Patches for payloadFile(pointer, cb)
patch_payloadFile_COMPRESSED = b"fs.writeFileSync('d-'+z,target2,'binary');"
patch_payloadFile_NONE = b"fs.writeFileSync('d-'+z+'.br',target,'binary');"

# Patches for payloadFileSync(pointer)
patch_payloadFileSync_COMPRESSED = b"fs.writeFileSync('d-'+z,target1,'binary');"
patch_payloadFileSync_NONE = b"fs.writeFileSync('d-'+z,target,'binary');"

# Patch payloadFile(pointer, cb)
p = src.find(b'payloadCopyMany(pointer, target, 0, 0, (error) => {')
p += len(b'payloadCopyMany(pointer, target, 0, 0, (error) => {')
src = src[:p] + patch__FILENAME+patch_payloadFile_NONE + src[p:]
PATCHED_BYTES += len(patch__FILENAME+patch_payloadFile_NONE)

p = src.find(b'payloadCopyManySync(pointer, target, 0, 0);')
p += len(b'payloadCopyManySync(pointer, target, 0, 0);')
src = src[:p] + patch__FILENAME+patch_payloadFile_NONE + src[p:]
PATCHED_BYTES += len(patch__FILENAME+patch_payloadFile_NONE)


# We want to avoid actually running code, might be dangeröus owo
# Didn't find a good place to prevent this. Ideally, we'd like to
# never even run the binary, but I'm lazy. Disable this only if you're
# sure. also. no guarantees in the first place.
if PREVENT_EXECUTION:
    p1 = src.find(b'return wrapper.apply(this.exports, args);')
    src = src[:p1] + b'return;' + src[p1:]
    PATCHED_BYTES += len(b'return;')

# Remove some bytes
p = src.find(b'// TODO move to some test')

if PATCHED_BYTES > 0:
    del src[p:p+PATCHED_BYTES]
else:
    src = src[:p] + b'F'*(-PATCHED_BYTES) + src[p:]

print("len before %d len after %d" % (LEN, len(src)))

dest_fd = open(FILENAME+'.PATCHED.exe', "wb")
dest_fd.write(src)
dest_fd.close()
