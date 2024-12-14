use std::{
    collections::{HashMap, HashSet},
    fs::read_to_string,
};

use macroquad::{
    camera::{set_camera, set_default_camera, Camera2D},
    color::{BLACK, GREEN, RED, WHITE},
    input::{
        is_key_pressed, is_mouse_button_down, is_mouse_button_pressed, mouse_position, mouse_wheel,
        KeyCode, MouseButton,
    },
    math::vec2,
    shapes::{draw_line, draw_rectangle},
    text::draw_text,
    time::get_frame_time,
    window::{clear_background, next_frame, screen_height, screen_width},
};

enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Clone)]
struct Fence {
    x1: f32,
    y1: f32,
    x2: f32,
    y2: f32,
}

fn parse_input() -> HashMap<(usize, usize), char> {
    let mut vegetable_locations = HashMap::new();
    read_to_string("input/day12")
        .unwrap()
        .lines()
        .enumerate()
        .for_each(|(y, line)| {
            line.chars().enumerate().for_each(|(x, character)| {
                vegetable_locations.insert((x, y), character);
            });
        });
    vegetable_locations
}

fn map_fencing(
    vegetable_locations: &HashMap<(usize, usize), char>,
    search_from: (usize, usize),
) -> (HashSet<(usize, usize)>, Vec<Fence>) {
    let search_character = vegetable_locations.get(&search_from).unwrap();
    let mut visited = HashSet::new();
    let mut fences = Vec::new();
    let mut next_search_from = HashSet::from([search_from]);
    loop {
        if next_search_from.is_empty() {
            break;
        }
        let mut new_next_search_from = HashSet::new();
        for now_search_from in next_search_from.clone() {
            visited.insert(now_search_from);
            let checks = vec![
                (
                    (now_search_from.0 as i32, now_search_from.1 as i32 + 1),
                    Direction::Down,
                ),
                (
                    (now_search_from.0 as i32, now_search_from.1 as i32 - 1),
                    Direction::Up,
                ),
                (
                    (now_search_from.0 as i32 + 1, now_search_from.1 as i32),
                    Direction::Right,
                ),
                (
                    (now_search_from.0 as i32 - 1, now_search_from.1 as i32),
                    Direction::Left,
                ),
            ];
            for i32_check in checks {
                if i32_check.0 .0 == -1 {
                    fences.push(Fence {
                        x1: (i32_check.0 .0 as f32 * 32.) + 30.,
                        y1: (i32_check.0 .1 as f32 * 32.),
                        x2: (i32_check.0 .0 as f32 * 32.) + 30.,
                        y2: (i32_check.0 .1 as f32 * 32.) + 32.,
                    });
                    continue;
                }
                if i32_check.0 .1 == -1 {
                    fences.push(Fence {
                        x1: (i32_check.0 .0 as f32 * 32.),
                        y1: (i32_check.0 .1 as f32 * 32.) + 30.,
                        x2: (i32_check.0 .0 as f32 * 32.) + 32.,
                        y2: (i32_check.0 .1 as f32 * 32.) + 30.,
                    });
                    continue;
                }

                let check = (
                    (i32_check.0 .0 as usize, i32_check.0 .1 as usize),
                    i32_check.1,
                );
                if vegetable_locations.get(&check.0).unwrap_or(&'.') == search_character {
                    if visited.contains(&check.0) {
                        continue;
                    }
                    new_next_search_from.insert(check.0);
                } else {
                    match check.1 {
                        Direction::Up => fences.push(Fence {
                            x1: (check.0 .0 as f32 * 32.),
                            y1: (check.0 .1 as f32 * 32.) + 32.,
                            x2: (check.0 .0 as f32 * 32.) + 32.,
                            y2: (check.0 .1 as f32 * 32.) + 32.,
                        }),
                        Direction::Down => fences.push(Fence {
                            x1: (check.0 .0 as f32 * 32.),
                            y1: (check.0 .1 as f32 * 32.) - 1.,
                            x2: (check.0 .0 as f32 * 32.) + 32.,
                            y2: (check.0 .1 as f32 * 32.) - 1.,
                        }),
                        Direction::Left => fences.push(Fence {
                            x1: (check.0 .0 as f32 * 32.) + 32.,
                            y1: (check.0 .1 as f32 * 32.),
                            x2: (check.0 .0 as f32 * 32.) + 32.,
                            y2: (check.0 .1 as f32 * 32.) + 32.,
                        }),
                        Direction::Right => fences.push(Fence {
                            x1: (check.0 .0 as f32 * 32.) - 1.,
                            y1: (check.0 .1 as f32 * 32.),
                            x2: (check.0 .0 as f32 * 32.) - 1.,
                            y2: (check.0 .1 as f32 * 32.) + 32.,
                        }),
                    }
                }
            }
            next_search_from = new_next_search_from
                .clone()
                .into_iter()
                .filter(|x| !visited.contains(x))
                .collect();
        }
    }
    (visited, fences)
}

pub async fn solve(camera: &mut Camera2D) {
    let vegetable_locations = parse_input();
    let mut current_cost = 0;
    let mut selected_group: Option<i32> = None;
    let mut grouped: HashMap<(usize, usize), i32> = HashMap::new();
    let mut group_fences: Vec<Vec<Fence>> = Vec::new();
    let mut camera_x = 0.0;
    let mut camera_y = 0.0;
    let mut camera_zoom = 1.0;
    let mut last_mouse_position: Option<(f32, f32)> = None;

    let ui_box_width = 500.0;
    let ui_box_height = 110.0;
    let ui_box_margin = 10.0;

    let mut fps_accumulator = 0;
    let mut fps_counter = 0;
    let mut elapsed_time = 0.0;

    loop {
        clear_background(BLACK);
        /* Track FPS */
        elapsed_time += get_frame_time();
        if elapsed_time > 1.0 {
            elapsed_time = 0.0;
            fps_counter = fps_accumulator;
            fps_accumulator = 0;
        } else {
            fps_accumulator += 1;
        }

        /* INPUT AND UPDATE */
        if is_mouse_button_down(MouseButton::Right) {
            let mouse_position = mouse_position();
            if let Some(last_position) = last_mouse_position {
                let delta_x = mouse_position.0 - last_position.0;
                let delta_y = mouse_position.1 - last_position.1;

                camera_x -= delta_x;
                camera_y -= delta_y;
            }
            last_mouse_position = Some(mouse_position);
        } else {
            last_mouse_position = None;
        }

        let mouse_wheel = mouse_wheel().1;
        if mouse_wheel != 0.0 {
            camera_zoom *= 1.0 + mouse_wheel * 0.1;
            camera_zoom = camera_zoom.clamp(0.5, 5.0);
        }
        camera.zoom = vec2(1.0 / screen_width(), 1.0 / screen_height()) * camera_zoom;
        camera.target = vec2(camera_x, camera_y);
        set_camera(camera);

        if is_mouse_button_pressed(MouseButton::Left) {
            let mouse_screen = mouse_position();
            let mouse_position = camera.screen_to_world(vec2(mouse_screen.0, mouse_screen.1));
            let snap_to_grid_position = (
                (mouse_position.x / 32.).floor() as usize,
                (mouse_position.y / 32.).floor() as usize,
            );
            if grouped.contains_key(&snap_to_grid_position) {
                selected_group = grouped.get(&snap_to_grid_position).copied();
            } else if snap_to_grid_position.0 < 140 && snap_to_grid_position.1 < 140 {
                grouped.insert(snap_to_grid_position, group_fences.len() as i32);
                selected_group = Some(group_fences.len() as i32);
                let (group, fences) = map_fencing(&vegetable_locations, snap_to_grid_position);
                for tile in group {
                    grouped.insert(tile, selected_group.unwrap());
                }
                group_fences.push(fences);
            }
            current_cost = (0..group_fences.len())
                .map(|id| {
                    grouped
                        .clone()
                        .into_iter()
                        .into_iter()
                        .filter(|(_, group)| *group as usize == id)
                        .collect::<Vec<_>>()
                        .len() as i32
                        * group_fences[id].len() as i32
                })
                .sum::<i32>()
        }
        if is_key_pressed(KeyCode::Escape) {
            return;
        }

        /* DRAW */
        if let Some(selected) = selected_group {
            for fence in &mut group_fences[selected as usize] {
                draw_line(fence.x1, fence.y1, fence.x2, fence.y2, 4., RED);
            }
        }
        for ((x, y), vegetable) in &vegetable_locations {
            draw_text(
                &vegetable.to_string(),
                *x as f32 * 32. + 8.,
                *y as f32 * 32. + 24.,
                32.,
                if grouped.contains_key(&(*x, *y)) {
                    GREEN
                } else {
                    WHITE
                },
            );
        }

        /* DRAW UI */
        set_default_camera();

        draw_rectangle(
            screen_width() - ui_box_width - ui_box_margin,
            ui_box_margin,
            ui_box_width,
            ui_box_height,
            WHITE,
        );
        draw_rectangle(
            screen_width() - ui_box_width - ui_box_margin + 5.0,
            ui_box_margin + 5.0,
            ui_box_width - 10.0,
            ui_box_height - 10.0,
            BLACK,
        );
        draw_text(
            &format!("FPS: {}", fps_counter),
            screen_width() - ui_box_width - ui_box_margin + 15.0,
            ui_box_margin + 30.0,
            25.0,
            WHITE,
        );
        draw_text(
            &format!(
                "Mapped tiles: {:.1}%",
                (grouped.len() as f32 / (140. * 140.)) * 100.
            ),
            screen_width() - ui_box_width - ui_box_margin + 15.0,
            ui_box_margin + 60.0,
            25.0,
            WHITE,
        );
        draw_text(
            &format!("Cost: {} $", current_cost),
            screen_width() - ui_box_width - ui_box_margin + 15.0,
            ui_box_margin + 90.0,
            25.0,
            WHITE,
        );
        next_frame().await;
    }
}
