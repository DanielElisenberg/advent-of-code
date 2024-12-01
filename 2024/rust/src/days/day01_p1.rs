use std::fs::read_to_string;

use macroquad::{
    camera::{set_camera, Camera2D},
    color::{BLACK, WHITE},
    input::{is_key_pressed, KeyCode},
    math::Vec2,
    shapes::draw_rectangle,
    text::draw_text,
    time::get_frame_time,
    window::{clear_background, next_frame},
};

pub struct NumberSquare {
    pub number: i32,
    pub color: macroquad::color::Color,
    pub sprite_size: f32,
    pub position: Vec2,
    pub visible: bool,
}

pub trait Drawable {
    fn draw(&self) {}
}

impl Drawable for NumberSquare {
    fn draw(&self) {
        if !self.visible {
            return;
        }
        draw_rectangle(
            self.position.x,
            self.position.y,
            self.sprite_size,
            self.sprite_size,
            self.color,
        );
        draw_text(
            &self.number.to_string(),
            self.position.x + self.sprite_size / 4.0,
            self.position.y + self.sprite_size / 1.5,
            self.sprite_size / 4.0,
            BLACK,
        );
    }
}

struct Lists {
    first: Vec<NumberSquare>,
    second: Vec<NumberSquare>,
    distances: Vec<NumberSquare>,
}

fn parse_input() -> Lists {
    let mut first_list = Vec::new();
    let mut second_list = Vec::new();
    read_to_string("input/day01")
        .unwrap()
        .lines()
        .for_each(|s| {
            let split_line = s.split("   ").collect::<Vec<&str>>();
            first_list.push(split_line[0].parse::<i32>().unwrap());
            second_list.push(split_line[1].parse::<i32>().unwrap());
        });
    first_list.sort();
    second_list.sort();
    let distances = first_list
        .clone()
        .into_iter()
        .enumerate()
        .map(|(index, value)| NumberSquare {
            number: (value - second_list[index]).abs(),
            color: macroquad::color::BLUE,
            sprite_size: 100.,
            position: Vec2::new(670., 400. + (index as f32) * 110.),
            visible: false,
        })
        .collect::<Vec<NumberSquare>>();

    return Lists {
        first: first_list
            .into_iter()
            .enumerate()
            .map(|(index, number)| NumberSquare {
                number,
                color: macroquad::color::WHITE,
                sprite_size: 100.,
                position: Vec2::new(560., 400. + (index as f32) * 110.),
                visible: true,
            })
            .collect(),
        second: second_list
            .into_iter()
            .enumerate()
            .map(|(index, number)| NumberSquare {
                number,
                color: macroquad::color::WHITE,
                sprite_size: 100.,
                position: Vec2::new(780., 400. + (index as f32) * 110.),
                visible: true,
            })
            .collect(),
        distances,
    };
}

enum ProcessState {
    Calculating,
    Sliding,
    Paused,
}

pub async fn solve(camera: &Camera2D) {
    let mut lists = parse_input();
    let length = lists.first.len();
    let mut target = 0;
    let mut state = ProcessState::Calculating;
    let mut sum_number = NumberSquare {
        number: 0,
        color: macroquad::color::BLUE,
        sprite_size: 200.,
        position: Vec2::new(100., 540.),
        visible: true,
    };
    set_camera(camera);
    loop {
        clear_background(BLACK);
        draw_text(
            &format!("The solution for Day 1 Part 1"),
            20.,
            40.,
            30.,
            WHITE,
        );
        draw_text("Press ESC to return to the menu", 20., 80., 20., WHITE);
        if is_key_pressed(KeyCode::Escape) {
            return;
        }

        let delta_time = get_frame_time();
        state = match state {
            ProcessState::Paused => ProcessState::Paused,
            ProcessState::Calculating => {
                lists.distances[target].visible = true;
                sum_number.number += lists.distances[target].number;
                target += 1;
                if target < length {
                    ProcessState::Sliding
                } else {
                    ProcessState::Paused
                }
            }
            ProcessState::Sliding => {
                for ns in &mut lists.first {
                    ns.position.y -= 1. * delta_time * 200.
                }
                for ns in &mut lists.second {
                    ns.position.y -= 1. * delta_time * 200.
                }
                for ns in &mut lists.distances {
                    ns.position.y -= 1. * delta_time * 200.
                }
                if lists.first[target].position.y <= 400. {
                    ProcessState::Calculating
                } else {
                    ProcessState::Sliding
                }
            }
        };
        for ns in &lists.first {
            ns.draw()
        }
        for ns in &lists.second {
            ns.draw()
        }
        for ns in &lists.distances {
            ns.draw()
        }

        sum_number.draw();

        next_frame().await;
    }
}
