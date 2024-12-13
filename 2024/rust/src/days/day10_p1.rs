use core::f32;
use std::collections::HashSet;
use std::fs::read_to_string;

use macroquad::camera::{set_camera, Camera3D};
use macroquad::prelude::*;

fn parse_input() -> Vec<Vec<f32>> {
    read_to_string("input/day10")
        .unwrap()
        .lines()
        .map(|line| {
            line.chars()
                .map(|ch| ch.to_digit(10).unwrap() as f32)
                .collect::<Vec<f32>>()
        })
        .collect::<Vec<Vec<f32>>>()
}

fn find_trailheads(cube_heights: &Vec<Vec<f32>>) -> Vec<(i32, i32)> {
    cube_heights
        .clone()
        .into_iter()
        .enumerate()
        .map(|(y, row)| {
            row.into_iter()
                .enumerate()
                .filter_map(|(x, height)| {
                    if height == 0.0 {
                        Some((y as i32, x as i32))
                    } else {
                        None
                    }
                })
                .collect::<Vec<(i32, i32)>>()
        })
        .flatten()
        .collect()
}

pub async fn solve(camera2d: &Camera2D) {
    let color_gradient = vec![
        WHITE,
        GREEN,
        Color::new(0.8, 1.0, 0.0, 1.0),
        Color::new(0.6, 0.8, 0.0, 1.0),
        Color::new(0.4, 0.6, 0.0, 1.0),
        Color::new(0.2, 0.4, 0.0, 1.0),
        Color::new(0.2, 0.0, 0.0, 1.0),
        Color::new(0.4, 0.0, 0.0, 1.0),
        Color::new(0.6, 0.0, 0.0, 1.0),
        RED,
    ];
    let ground_size = 54;
    let cube_heights = parse_input();

    let mut camera_distance = 200.0;
    let mut camera_angle_horizontal = 0.0;
    let mut camera_angle_vertical = 75.0_f32.to_radians();
    let focus_point = vec3(26.0, 0.0, 26.0);

    let mut last_frame_mouse_position = mouse_position();

    let mut trailhead_sum = 0;
    let mut trailheads = find_trailheads(&cube_heights);
    let mut search_cubes: Vec<(i32, i32)> = vec![trailheads.pop().unwrap()];
    let mut visited: Vec<(i32, i32)> = Vec::new();
    let mut finished = false;

    loop {
        clear_background(SKYBLUE);

        /* INPUT & UPDATE */
        let mouse_delta = (
            mouse_position().0 - last_frame_mouse_position.0,
            mouse_position().1 - last_frame_mouse_position.1,
        );
        last_frame_mouse_position = mouse_position();
        camera_distance -= mouse_wheel().1 * 0.5;
        camera_distance = camera_distance.clamp(1.0, 200.0);
        if is_mouse_button_down(MouseButton::Right) {
            camera_angle_horizontal += mouse_delta.0 * 0.01;

            camera_angle_vertical -= mouse_delta.1 * 0.01;
            camera_angle_vertical =
                camera_angle_vertical.clamp(5.0_f32.to_radians(), 85.0_f32.to_radians());
        }
        if is_key_pressed(KeyCode::Escape) {
            return;
        }
        if is_key_down(KeyCode::F) && !finished {
            search_cubes = search_cubes
                .into_iter()
                .map(|search_cube| {
                    visited.push((search_cube.1, search_cube.0));
                    vec![
                        (search_cube.0, search_cube.1 - 1),
                        (search_cube.0, search_cube.1 + 1),
                        (search_cube.0 - 1, search_cube.1),
                        (search_cube.0 + 1, search_cube.1),
                    ]
                    .into_iter()
                    .filter(|(x, y)| {
                        *x >= 0
                            && *x < cube_heights.len() as i32
                            && *y >= 0
                            && *y < cube_heights.len() as i32
                            && !visited.contains(&(*y, *x))
                    })
                    .filter(|(x, y)| {
                        cube_heights[*x as usize][*y as usize]
                            == cube_heights[search_cube.0 as usize][search_cube.1 as usize] + 1.
                    })
                    .collect::<Vec<(i32, i32)>>()
                })
                .flatten()
                .collect::<Vec<(i32, i32)>>();

            if search_cubes.is_empty() {
                match trailheads.pop() {
                    Some(trailhead) => {
                        search_cubes.push(trailhead);
                        visited = Vec::new();
                    }
                    None => {
                        finished = true;
                    }
                }
            } else {
                let mut check_cubes = search_cubes.clone();
                let mut dedup = HashSet::new();
                check_cubes.retain(|search_cube| dedup.insert(*search_cube));
                trailhead_sum += check_cubes
                    .clone()
                    .into_iter()
                    .filter(|search_cube| {
                        if cube_heights[search_cube.0 as usize][search_cube.1 as usize] == 9. {
                            true
                        } else {
                            false
                        }
                    })
                    .collect::<Vec<(i32, i32)>>()
                    .len() as i32;
            }
        }
        /* CAMERA */
        let camera_position = vec3(
            focus_point.x
                + camera_distance * camera_angle_horizontal.cos() * camera_angle_vertical.sin(),
            focus_point.y + camera_distance * camera_angle_vertical.cos(),
            focus_point.z
                + camera_distance * camera_angle_horizontal.sin() * camera_angle_vertical.sin(),
        );

        let camera3d = Camera3D {
            position: camera_position,
            up: vec3(0.0, 1.0, 0.0),
            target: focus_point,
            ..Default::default()
        };
        set_camera(&camera3d);

        /* DRAW */
        draw_plane(
            vec3(26.0, 0.0, 26.0),
            vec2(
                (ground_size as f32 / 2.0) + 5.0,
                (ground_size as f32 / 2.0) + 5.0,
            ),
            None,
            WHITE,
        );
        for (z, row) in cube_heights.iter().enumerate() {
            for (x, &height) in row.iter().enumerate() {
                draw_cube(
                    vec3(x as f32, height as f32 / 2.0, z as f32),
                    vec3(1.0, height as f32 + 0.2, 1.0),
                    None,
                    if visited.contains(&(x as i32, z as i32)) {
                        BLUE
                    } else {
                        color_gradient[height as usize]
                    },
                );
                draw_cube_wires(
                    vec3(x as f32, height as f32 / 2.0, z as f32),
                    vec3(1., height as f32, 1.),
                    BLACK,
                );
            }
        }
        for (x, y) in search_cubes.iter() {
            draw_cube(
                vec3(
                    *y as f32,
                    cube_heights[*x as usize][*y as usize] as f32 + 1.,
                    *x as f32,
                ),
                vec3(0.5, 0.5, 0.5),
                None,
                BLUE,
            );
        }
        set_camera(camera2d);
        draw_text(
            &format!("Trailhead sum: {}", trailhead_sum),
            10.,
            50.,
            35.,
            BLACK,
        );
        draw_text(&"Hold <F> to explore the trails", 10., 150., 35., BLACK);

        next_frame().await;
    }
}
