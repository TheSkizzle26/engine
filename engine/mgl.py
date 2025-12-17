import moderngl
import engine
from cffi import FFI


def load_program(ctx, vert_path, frag_path):
    with open(vert_path) as file:
        vert = file.read()
    with open(frag_path) as file:
        frag = file.read()

    return ctx.program(vert, frag)

def rl_tex_to_mgl_tex(ctx, tex):
    ffi = FFI()

    image = engine.load_image_from_texture(tex)
    engine.image_format(image, engine.PixelFormat.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)
    data = ffi.buffer(image.data, image.width * image.height * 4)

    gl_tex = ctx.texture((tex.width, tex.height), 4, data=data)
    gl_tex.filter = (ctx.NEAREST, ctx.NEAREST)

    engine.unload_image(image)
    return gl_tex