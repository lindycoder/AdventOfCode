use std::env;

mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod day07;
mod day08;
mod day09;
#[macro_use]
mod tools;

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
        "day05.1" => day05::version1,
        "day05.2" => day05::version2,
        "day06.1" => day06::version1,
        "day06.2" => day06::version2,
        "day07.1" => day07::version1,
        "day07.2" => day07::version2,
        "day08.1" => day08::version1,
        "day08.2" => day08::version2,
        "day09.1" => day09::version1,
        "day09.2" => day09::version2,
        &_ => day09::version1,
    };

    let r = target_fn(None);
    println!("{r}");
}
