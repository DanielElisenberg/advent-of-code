use macroquad::{
    camera::{set_camera, Camera2D},
    color::{BLACK, WHITE},
    input::{is_key_pressed, KeyCode},
    text::draw_text,
    window::{clear_background, next_frame},
};

fn parse_input() -> String {
    "".to_owned()
}

pub async fn solve(camera: &Camera2D) {
    let _input = parse_input();

    loop {
        clear_background(BLACK);
        set_camera(camera);

        draw_text(&format!("The solution for Day XX"), 20., 40., 30., WHITE);
        draw_text("Press ESC to return to the menu", 20.0, 80.0, 20.0, WHITE);

        if is_key_pressed(KeyCode::Escape) {
            return;
        }
        next_frame().await;
    }
}
