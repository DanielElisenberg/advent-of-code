pub mod days;
use macroquad::prelude::*;

#[derive(PartialEq, Clone, Copy)]
enum GameState {
    Menu,
    Day1Part1,
    Day1Part2,
}

fn window_conf() -> Conf {
    Conf {
        window_title: "Advent of Code".to_owned(),
        window_width: 1920,
        window_height: 1080,
        fullscreen: false,
        ..Default::default()
    }
}

#[macroquad::main(window_conf)]
async fn main() {
    let default_camera_target = vec2(screen_width() / 2., screen_height() / 2.);
    let mut state = GameState::Menu;
    let mut camera = Camera2D {
        target: default_camera_target,
        zoom: vec2(1.0 / screen_width() * 2.0, 1.0 / screen_height() * 2.0),
        ..Default::default()
    };
    let mut selected_day = 0;
    let days = vec![GameState::Day1Part1, GameState::Day1Part2];

    loop {
        clear_background(BLACK);
        camera.target = default_camera_target;
        match state {
            GameState::Menu => {
                if is_key_pressed(KeyCode::Right) && selected_day < 25 {
                    selected_day += 1;
                }
                if is_key_pressed(KeyCode::Left) && selected_day > 0 {
                    selected_day -= 1;
                }
                camera.target.x = (screen_width() / 2.) + 100. * (selected_day as f32);
                set_camera(&camera);
                draw_text("Main Menu", 20.0, 40.0, 30.0, WHITE);
                if is_key_pressed(KeyCode::Enter) {
                    state = days[selected_day];
                }
            }
            GameState::Day1Part1 => {
                days::day01_p1::solve(&camera).await;
                state = GameState::Menu;
            }
            GameState::Day1Part2 => {
                days::day01_p2::solve(&camera).await;
                state = GameState::Menu;
            }
        }
        next_frame().await;
    }
}
