use std::env;

mod day01;

fn main() {
    println!("Hello, world2!");
    let args: Vec<String> = env::args().collect();
    let target: &str;
    if args.len() >= 2 {
        target = &args[1];
    } else {
        target = "no target";
    }

    println!("Running {target}");

    let target_fn = match target {
        "day01.1" => day01::version1,
        "day01.2" => day01::version2,
        &_ => day01::version2
    };

    let r = target_fn(None);
    println!("{r}");
}
