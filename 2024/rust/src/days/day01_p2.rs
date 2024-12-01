use std::{collections::HashMap, fs::read_to_string};

use macroquad::{
    camera::{set_camera, Camera2D},
    color::{BLACK, WHITE},
    input::{is_key_pressed, KeyCode},
    text::draw_text,
    window::{clear_background, next_frame},
};

fn parse_input() -> i32 {
    let mut first_list = Vec::new();
    let mut occurrences = HashMap::new();
    read_to_string("input/day01")
        .unwrap()
        .lines()
        .for_each(|s| {
            let split_line = s.split("   ").collect::<Vec<&str>>();
            first_list.push(split_line[0].parse::<i32>().unwrap());
            *occurrences
                .entry(split_line[1].parse::<i32>().unwrap())
                .or_insert(0) += 1;
        });
    let similarity = first_list
        .into_iter()
        .map(|num| num * occurrences.get(&num).unwrap_or(&0))
        .sum::<i32>();
    similarity
}

pub async fn solve(camera: &Camera2D) {
    let similarity = parse_input();
    set_camera(camera);
    loop {
        clear_background(BLACK);
        draw_text(
            &format!("The solution for Day 1 Part 2"),
            20.,
            40.,
            30.,
            WHITE,
        );
        draw_text("Press ESC to return to the menu", 20., 80., 20., WHITE);
        draw_text(
            &format!("Similarity: {}", similarity),
            20.,
            120.,
            20.,
            WHITE,
        );

        if is_key_pressed(KeyCode::Escape) {
            return;
        }
        next_frame().await;
    }
}
