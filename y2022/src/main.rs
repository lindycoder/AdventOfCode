extern crate core;

use std::env;

mod day01;
mod day02;
mod day03;
mod day04;

fn main() {
    println!("Hello, world2!");
    let args: Vec<String> = env::args().collect();
    let target = if args.len() >= 2 {
        &args[1]
    } else {
        "no target"
    };

    println!("Running {target}");

    let target_fn = match target {
        "day01.1" => day01::version1,
        "day01.2" => day01::version2,
        "day02.1" => day02::version1,
        "day02.2" => day02::version2,
        "day03.1" => day03::version1,
        "day03.2" => day03::version2,
        "day04.1" => day04::version1,
        "day04.2" => day04::version2,
        &_ => day04::version2,
    };

    let r = target_fn(None);
    println!("{r}");
}
