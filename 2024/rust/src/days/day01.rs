use std::fs::read_to_string;

use macroquad::{
    camera::{set_camera, Camera2D},
    color::{BLACK, WHITE},
    input::{is_key_pressed, KeyCode},
    text::draw_text,
    window::{clear_background, next_frame},
};

fn parse_input() -> String {
    read_to_string("input/day01").unwrap()
}

pub async fn solve(camera: &Camera2D) {
    let _input = parse_input();
    set_camera(camera);
    loop {
        clear_background(BLACK);
        draw_text(&format!("The solution for Day 1"), 20., 40., 30., WHITE);
        draw_text("Press ESC to return to the menu", 20., 80., 20., WHITE);

        if is_key_pressed(KeyCode::Escape) {
            return;
        }
        next_frame().await;
    }
}
