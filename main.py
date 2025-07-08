import pyray as rl

rl.init_window(500, 500, "Bits")

heart = rl.load_texture("./data/heart.png")

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.WHITE)
    rl.draw_text("I love you deekshu", 50, 200, 30, rl.BLACK)
    rl.draw_texture_ex(heart, rl.Vector2(350, 170), 0, 0.2, rl.WHITE)
    rl.end_drawing()
rl.unload_texture(heart)
rl.close_window()
