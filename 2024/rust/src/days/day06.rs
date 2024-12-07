use std::{collections::HashSet, fs::read_to_string};

use macroquad::{
    camera::{set_camera, Camera2D},
    color::{BLACK, GRAY, RED, WHITE},
    input::{is_key_pressed, KeyCode},
    math::{vec2, Vec2},
    shapes::draw_rectangle,
    text::draw_text,
    texture::{draw_texture, load_texture, Texture2D},
    time::get_frame_time,
    window::{clear_background, next_frame, screen_height, screen_width},
};

const MAP_SIZE: i32 = 130;

fn parse_input() -> (HashSet<(i32, i32)>, (i32, i32)) {
    let mut player_location: (i32, i32) = (0, 0);
    let mut crate_locations: HashSet<(i32, i32)> = HashSet::new();

    read_to_string("input/day06")
        .unwrap()
        .lines()
        .enumerate()
        .for_each(|(y, line)| {
            line.chars()
                .into_iter()
                .enumerate()
                .for_each(|(x, character)| {
                    if character == '#' {
                        crate_locations.insert((x as i32, y as i32));
                    } else if character == '^' {
                        player_location = (x as i32, y as i32)
                    }
                });
        });
    return (crate_locations, player_location);
}

enum GuardDirection {
    Up,
    Down,
    Left,
    Right,
}

fn find_new_target(
    player_location: &(i32, i32),
    player_direction: &GuardDirection,
    crate_locations: &HashSet<(i32, i32)>,
) -> Result<(i32, i32), GuardDirection> {
    match player_direction {
        GuardDirection::Up => {
            if !crate_locations.contains(&(player_location.0, player_location.1 - 1)) {
                Ok((player_location.0, player_location.1 - 1))
            } else {
                Err(GuardDirection::Right)
            }
        }
        GuardDirection::Down => {
            if !crate_locations.contains(&(player_location.0, player_location.1 + 1)) {
                Ok((player_location.0, player_location.1 + 1))
            } else {
                Err(GuardDirection::Left)
            }
        }
        GuardDirection::Left => {
            if !crate_locations.contains(&(player_location.0 - 1, player_location.1)) {
                Ok((player_location.0 - 1, player_location.1))
            } else {
                Err(GuardDirection::Up)
            }
        }
        GuardDirection::Right => {
            if !crate_locations.contains(&(player_location.0 + 1, player_location.1)) {
                Ok((player_location.0 + 1, player_location.1))
            } else {
                Err(GuardDirection::Down)
            }
        }
    }
}

struct Guard {
    pub target: Option<Vec2>,
    pub position: Vec2,
    pub direction: GuardDirection,
    pub walking_speed: f32,
    pub animation_speed: f32,
    pub animation_countdown: f32,
    pub current_frame: usize,
    pub animation_frames: Vec<Texture2D>,
}

impl Guard {
    fn get_grid_position(self: &Self) -> (i32, i32) {
        return (
            (self.position.x / 32.) as i32,
            (self.position.y / 32.) as i32,
        );
    }

    fn update(self: &mut Self, delta_time: f32) -> bool {
        let reached_target = match self.target {
            None => true,
            Some(target) => {
                let direction = (target - self.position).normalize();
                let movement = direction * self.walking_speed * delta_time;
                if (self.position + movement - target).length() > (self.position - target).length()
                {
                    self.position = target;
                    self.target = None;
                    true
                } else {
                    self.position += movement;
                    false
                }
            }
        };
        self.animation_countdown -= delta_time;
        let switch = if self.animation_countdown < 0. {
            self.animation_countdown = self.animation_speed;
            true
        } else {
            false
        };
        match &self.direction {
            GuardDirection::Up => {
                self.current_frame = if switch && self.current_frame == 5 {
                    4
                } else if switch {
                    5
                } else {
                    self.current_frame
                }
            }
            GuardDirection::Down => {
                self.current_frame = if switch && self.current_frame == 7 {
                    6
                } else if switch {
                    7
                } else {
                    self.current_frame
                }
            }
            GuardDirection::Left => {
                self.current_frame = if switch && self.current_frame == 3 {
                    2
                } else if switch {
                    3
                } else {
                    self.current_frame
                }
            }
            GuardDirection::Right => {
                self.current_frame = if switch && self.current_frame == 1 {
                    0
                } else if switch {
                    1
                } else {
                    self.current_frame
                }
            }
        };
        return reached_target;
    }

    fn change_direction(self: &mut Self, new_direction: GuardDirection) {
        self.direction = new_direction;
        self.animation_countdown = self.animation_speed;
        self.current_frame = match self.direction {
            GuardDirection::Up => 4,
            GuardDirection::Down => 6,
            GuardDirection::Left => 2,
            GuardDirection::Right => 0,
        };
    }

    fn draw(self: &Self) {
        draw_texture(
            &self.animation_frames[self.current_frame],
            self.position.x,
            self.position.y,
            WHITE,
        );
    }
}

pub async fn solve(camera: &mut Camera2D) {
    let (crate_locations, player_location) = parse_input();
    let mut footsteps: HashSet<(i32, i32)> = HashSet::new();
    footsteps.insert(player_location);
    let mut guard = Guard {
        target: None,
        position: vec2(
            player_location.0 as f32 * 32.,
            player_location.1 as f32 * 32.,
        ),
        direction: GuardDirection::Up,
        walking_speed: 200.,
        animation_speed: 0.25,
        animation_countdown: 0.0,
        current_frame: 0,
        animation_frames: vec![
            load_texture("assets/day06/guard/r1.png").await.unwrap(),
            load_texture("assets/day06/guard/r2.png").await.unwrap(),
            load_texture("assets/day06/guard/l1.png").await.unwrap(),
            load_texture("assets/day06/guard/l2.png").await.unwrap(),
            load_texture("assets/day06/guard/u1.png").await.unwrap(),
            load_texture("assets/day06/guard/u2.png").await.unwrap(),
            load_texture("assets/day06/guard/d1.png").await.unwrap(),
            load_texture("assets/day06/guard/d2.png").await.unwrap(),
        ],
    };

    let crate_texture = load_texture("assets/day06/crate.png").await.unwrap();
    let footsteps_texture = load_texture("assets/day06/footsteps.png").await.unwrap();
    let out_texture = load_texture("assets/day06/out.png").await.unwrap();

    let mut zoomed_in = true;
    camera.zoom = vec2(1.0 / screen_width() * 4.0, 1.0 / screen_height() * 4.0);
    set_camera(camera);

    enum ProcessState {
        FindingTarget,
        GuardWalking,
        GuardExited,
    }
    let mut state = ProcessState::FindingTarget;

    loop {
        let delta_time = get_frame_time();
        clear_background(GRAY);

        /* UPDATE */
        state = match state {
            ProcessState::FindingTarget => {
                let current_location = guard.get_grid_position();
                if current_location.0 == MAP_SIZE
                    || current_location.1 == MAP_SIZE
                    || current_location.0 == -1
                    || current_location.1 == -1
                {
                    ProcessState::GuardExited
                } else {
                    footsteps.insert((current_location.0, current_location.1));
                    match find_new_target(&current_location, &guard.direction, &crate_locations) {
                        Ok(target) => {
                            guard.target = Some(vec2(target.0 as f32 * 32., target.1 as f32 * 32.));
                            ProcessState::GuardWalking
                        }
                        Err(direction) => {
                            guard.change_direction(direction);
                            ProcessState::FindingTarget
                        }
                    }
                }
            }
            ProcessState::GuardWalking => {
                if guard.update(delta_time) {
                    ProcessState::FindingTarget
                } else {
                    ProcessState::GuardWalking
                }
            }
            ProcessState::GuardExited => ProcessState::GuardExited,
        };
        camera.target = guard.position;

        /* INPUT */
        if is_key_pressed(KeyCode::Escape) {
            return;
        }
        if is_key_pressed(KeyCode::Z) {
            if zoomed_in {
                camera.zoom = vec2(1.0 / screen_width() * 2.0, 1.0 / screen_height() * 2.0);
            } else {
                camera.zoom = vec2(1.0 / screen_width() * 4.0, 1.0 / screen_height() * 4.0);
            }
            zoomed_in = !zoomed_in;
        }
        set_camera(camera);

        /* DRAW */
        for location in -1..MAP_SIZE + 1 {
            draw_texture(&out_texture, -1. * 32., location as f32 * 32.0, WHITE);
            draw_texture(&out_texture, location as f32 * 32.0, -1. * 32., WHITE);
            draw_texture(
                &out_texture,
                (MAP_SIZE as f32) * 32.,
                location as f32 * 32.0,
                WHITE,
            );
            draw_texture(
                &out_texture,
                location as f32 * 32.0,
                (MAP_SIZE as f32) * 32.,
                WHITE,
            );
        }
        for crate_location in &crate_locations {
            draw_texture(
                &crate_texture,
                crate_location.0 as f32 * 32.0,
                crate_location.1 as f32 * 32.0,
                WHITE,
            );
        }
        for footstep in &footsteps {
            draw_texture(
                &footsteps_texture,
                footstep.0 as f32 * 32.0,
                footstep.1 as f32 * 32.0,
                RED,
            );
        }
        guard.draw();
        draw_text(
            &format!("Tiles stepped on: {}", &footsteps.len()),
            camera.target.x,
            camera.target.y + 500.,
            40.,
            WHITE,
        );
        next_frame().await;
    }
}
