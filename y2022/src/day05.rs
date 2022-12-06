use itertools::Itertools;
use regex::Regex;
use std::collections::HashMap;
use std::ops::Deref;

pub fn version1(input: Option<String>) -> String {
    let data = input.unwrap_or_else(puzzle_input);
    let parts: Vec<&str> = data.split("\n\n").collect();

    let mut crate_layout = parse_stacks(parts[0]);
    let actions = parse_actions(parts[1]);

    for (num, from, to) in actions {
        move_crates(num, from, to, &mut crate_layout)
    }

    crate_layout
        .keys()
        .sorted()
        .map(|k| *crate_layout[k].last().unwrap())
        .collect::<Vec<char>>()
        .iter()
        .collect()
}
pub fn version2(input: Option<String>) -> String {
    let data = input.unwrap_or_else(puzzle_input);
    let parts: Vec<&str> = data.split("\n\n").collect();

    let mut crate_layout = parse_stacks(parts[0]);
    let actions = parse_actions(parts[1]);

    for (num, from, to) in actions {
        move_crates_9001(num, from, to, &mut crate_layout)
    }

    crate_layout
        .keys()
        .sorted()
        .map(|k| *crate_layout[k].last().unwrap())
        .collect::<Vec<char>>()
        .iter()
        .collect()
}

fn parse_stacks(def: &str) -> HashMap<char, Vec<char>> {
    let lines_vec = def.lines().collect::<Vec<&str>>();
    let (name_line, crate_lines) = lines_vec.split_last().unwrap();

    let names: Vec<char> = name_line
        .deref()
        .split("   ")
        .map(|e| e.trim().chars().next().unwrap())
        .collect();

    let mut result: HashMap<char, Vec<char>> = names
        .iter()
        .map(|e| (*e, Vec::new() as Vec<char>))
        .into_iter()
        .collect();

    for line in crate_lines.iter().rev() {
        for (i, chunk) in line.chars().collect::<Vec<char>>().chunks(4).enumerate() {
            let crate_def: Vec<&char> = chunk.iter().filter(|c| matches!(*c, 'A'..='Z')).collect();
            if !crate_def.is_empty() {
                result
                    .get_mut(&names[i])
                    .unwrap()
                    .push(**crate_def.first().unwrap())
            }
        }
    }
    result
}

fn parse_actions(def: &str) -> Vec<(u32, char, char)> {
    let re = Regex::new(r"move (\d+) from (.) to (.)").unwrap();

    re.captures_iter(def)
        .map(|cap| {
            (
                cap[1].parse::<u32>().unwrap(),
                cap[2].chars().next().unwrap(),
                cap[3].chars().next().unwrap(),
            )
        })
        .collect()
}

fn move_crates(num: u32, from_stack: char, to_stack: char, stacks: &mut HashMap<char, Vec<char>>) {
    for _ in 0..num {
        let item = stacks.get_mut(&from_stack).unwrap().pop().unwrap();
        stacks.get_mut(&to_stack).unwrap().push(item);
    }
}

fn move_crates_9001(
    num: u32,
    from_stack: char,
    to_stack: char,
    stacks: &mut HashMap<char, Vec<char>>,
) {
    let source_stack = stacks.get_mut(&from_stack).unwrap();
    let moving = source_stack.split_off(source_stack.len() - num as usize);
    stacks.get_mut(&to_stack).unwrap().extend(moving);
}

#[cfg(test)]
mod tests {
    use crate::day05::{
        move_crates, move_crates_9001, parse_actions, parse_stacks, version1, version2,
    };
    use std::collections::HashMap;

    #[test]
    fn example_v1() {
        let input = "    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2";
        let result = version1(Some(input.to_string()));
        assert_eq!(result, "CMZ");
    }

    #[test]
    fn test_parse_stacks() {
        assert_eq!(
            parse_stacks(
                "    [D]
[N] [C]
[Z] [M] [P]
 1   2   3"
            ),
            HashMap::from([
                ('1', vec!['Z', 'N']),
                ('2', vec!['M', 'C', 'D']),
                ('3', vec!['P']),
            ])
        );
    }

    #[test]
    fn test_parse_actions() {
        assert_eq!(
            parse_actions(
                "move 1 from 2 to 1
move 3 from 1 to 3
move 133 from 1 to 3"
            ),
            vec![(1, '2', '1'), (3, '1', '3'), (133, '1', '3')]
        );
    }

    #[test]
    fn test_move_crates_1() {
        let mut stacks = HashMap::from([('1', vec!['a']), ('2', vec!['b'])]);
        move_crates(1, '2', '1', &mut stacks);
        assert_eq!(*stacks[&'1'], vec!['a', 'b']);
        assert_eq!(*stacks[&'2'], vec![] as Vec<char>);
    }

    #[test]
    fn test_move_crates_multi() {
        let mut stacks = HashMap::from([('1', vec!['a', 'c', 'd', 'f']), ('2', vec!['b'])]);
        move_crates(3, '1', '2', &mut stacks);
        assert_eq!(*stacks[&'1'], vec!['a']);
        assert_eq!(*stacks[&'2'], vec!['b', 'f', 'd', 'c']);
    }

    #[test]
    fn test_move_crates_9001_1() {
        let mut stacks = HashMap::from([('1', vec!['a']), ('2', vec!['b'])]);
        move_crates_9001(1, '2', '1', &mut stacks);
        assert_eq!(*stacks[&'1'], vec!['a', 'b']);
        assert_eq!(*stacks[&'2'], vec![] as Vec<char>);
    }

    #[test]
    fn test_move_crates_9001_multi() {
        let mut stacks = HashMap::from([('1', vec!['a', 'c', 'd', 'f']), ('2', vec!['b'])]);
        move_crates_9001(3, '1', '2', &mut stacks);
        assert_eq!(*stacks[&'1'], vec!['a']);
        assert_eq!(*stacks[&'2'], vec!['b', 'c', 'd', 'f']);
    }

    #[test]
    fn example_v2() {
        let input = "    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2";
        let result = version2(Some(input.to_string()));
        assert_eq!(result, "MCD");
    }
}

pub fn puzzle_input() -> String {
    String::from(
        "                    [Q]     [P] [P]
                [G] [V] [S] [Z] [F]
            [W] [V] [F] [Z] [W] [Q]
        [V] [T] [N] [J] [W] [B] [W]
    [Z] [L] [V] [B] [C] [R] [N] [M]
[C] [W] [R] [H] [H] [P] [T] [M] [B]
[Q] [Q] [M] [Z] [Z] [N] [G] [G] [J]
[B] [R] [B] [C] [D] [H] [D] [C] [N]
 1   2   3   4   5   6   7   8   9

move 3 from 6 to 2
move 5 from 6 to 7
move 6 from 2 to 5
move 1 from 9 to 7
move 1 from 1 to 9
move 1 from 5 to 3
move 1 from 2 to 5
move 3 from 4 to 5
move 10 from 7 to 3
move 1 from 4 to 9
move 6 from 8 to 7
move 4 from 7 to 8
move 1 from 7 to 3
move 1 from 1 to 2
move 1 from 2 to 8
move 1 from 9 to 1
move 3 from 9 to 4
move 4 from 8 to 3
move 4 from 7 to 1
move 4 from 4 to 6
move 2 from 8 to 7
move 9 from 3 to 8
move 2 from 7 to 4
move 3 from 4 to 9
move 4 from 1 to 9
move 4 from 3 to 9
move 2 from 1 to 4
move 1 from 4 to 6
move 3 from 3 to 2
move 1 from 2 to 8
move 1 from 2 to 7
move 3 from 6 to 2
move 2 from 6 to 7
move 4 from 2 to 3
move 3 from 7 to 9
move 2 from 5 to 6
move 15 from 9 to 4
move 4 from 9 to 2
move 12 from 5 to 4
move 9 from 8 to 5
move 25 from 4 to 7
move 1 from 4 to 7
move 1 from 4 to 8
move 2 from 2 to 5
move 1 from 4 to 2
move 23 from 7 to 6
move 2 from 5 to 2
move 22 from 6 to 8
move 4 from 5 to 9
move 1 from 7 to 9
move 2 from 6 to 4
move 2 from 4 to 7
move 25 from 8 to 3
move 1 from 2 to 1
move 3 from 2 to 3
move 1 from 6 to 8
move 1 from 1 to 8
move 1 from 2 to 8
move 1 from 8 to 1
move 4 from 5 to 7
move 1 from 8 to 4
move 5 from 9 to 8
move 5 from 8 to 9
move 1 from 8 to 5
move 3 from 5 to 4
move 3 from 9 to 1
move 30 from 3 to 4
move 3 from 1 to 4
move 2 from 9 to 5
move 4 from 7 to 9
move 16 from 4 to 8
move 6 from 3 to 9
move 3 from 7 to 3
move 19 from 4 to 7
move 8 from 9 to 4
move 1 from 1 to 9
move 13 from 7 to 9
move 3 from 7 to 8
move 3 from 5 to 9
move 4 from 8 to 3
move 2 from 7 to 3
move 14 from 9 to 4
move 10 from 3 to 1
move 12 from 4 to 8
move 6 from 1 to 9
move 1 from 1 to 2
move 1 from 7 to 1
move 6 from 9 to 3
move 17 from 8 to 6
move 10 from 8 to 5
move 1 from 7 to 8
move 1 from 9 to 5
move 2 from 3 to 1
move 4 from 5 to 9
move 1 from 8 to 7
move 6 from 9 to 7
move 4 from 4 to 2
move 3 from 4 to 6
move 4 from 5 to 9
move 4 from 9 to 3
move 1 from 2 to 4
move 4 from 4 to 7
move 3 from 5 to 3
move 1 from 4 to 5
move 5 from 1 to 2
move 1 from 1 to 9
move 7 from 2 to 7
move 1 from 5 to 7
move 8 from 3 to 5
move 20 from 6 to 7
move 9 from 7 to 9
move 2 from 2 to 9
move 2 from 3 to 1
move 2 from 1 to 3
move 2 from 3 to 4
move 2 from 4 to 6
move 1 from 3 to 9
move 1 from 4 to 9
move 1 from 6 to 9
move 2 from 5 to 8
move 2 from 8 to 5
move 1 from 6 to 7
move 2 from 5 to 8
move 6 from 9 to 5
move 2 from 8 to 6
move 11 from 9 to 2
move 1 from 6 to 5
move 11 from 2 to 5
move 1 from 6 to 4
move 7 from 5 to 9
move 7 from 9 to 1
move 1 from 4 to 9
move 28 from 7 to 5
move 1 from 7 to 5
move 5 from 5 to 9
move 5 from 9 to 3
move 6 from 1 to 8
move 1 from 1 to 7
move 5 from 3 to 2
move 1 from 7 to 8
move 7 from 8 to 1
move 1 from 9 to 4
move 2 from 2 to 5
move 22 from 5 to 3
move 1 from 7 to 8
move 1 from 4 to 7
move 1 from 8 to 9
move 1 from 9 to 4
move 14 from 5 to 7
move 5 from 5 to 9
move 19 from 3 to 4
move 1 from 2 to 9
move 2 from 2 to 5
move 1 from 5 to 1
move 6 from 1 to 7
move 2 from 7 to 6
move 1 from 1 to 9
move 2 from 5 to 8
move 8 from 4 to 5
move 3 from 4 to 7
move 3 from 3 to 5
move 2 from 8 to 9
move 16 from 7 to 5
move 9 from 4 to 6
move 22 from 5 to 3
move 1 from 5 to 8
move 1 from 8 to 7
move 10 from 3 to 4
move 1 from 5 to 4
move 10 from 4 to 5
move 8 from 5 to 2
move 5 from 2 to 7
move 5 from 7 to 1
move 4 from 7 to 6
move 3 from 9 to 7
move 2 from 2 to 3
move 3 from 5 to 1
move 6 from 9 to 7
move 5 from 7 to 8
move 6 from 1 to 5
move 6 from 3 to 4
move 4 from 4 to 2
move 1 from 4 to 6
move 5 from 8 to 7
move 3 from 2 to 3
move 1 from 1 to 4
move 1 from 1 to 9
move 2 from 2 to 1
move 2 from 4 to 3
move 4 from 3 to 7
move 3 from 7 to 3
move 13 from 6 to 1
move 1 from 9 to 2
move 6 from 3 to 5
move 8 from 1 to 4
move 1 from 2 to 7
move 9 from 4 to 9
move 7 from 5 to 1
move 2 from 5 to 6
move 1 from 1 to 4
move 1 from 4 to 3
move 2 from 1 to 2
move 5 from 3 to 6
move 2 from 6 to 1
move 13 from 7 to 6
move 2 from 3 to 4
move 2 from 2 to 9
move 2 from 7 to 8
move 6 from 9 to 2
move 1 from 9 to 3
move 1 from 5 to 2
move 7 from 1 to 2
move 1 from 6 to 7
move 1 from 4 to 8
move 1 from 3 to 1
move 1 from 7 to 8
move 7 from 1 to 9
move 4 from 8 to 6
move 1 from 5 to 3
move 9 from 9 to 5
move 1 from 1 to 2
move 14 from 2 to 7
move 2 from 9 to 3
move 13 from 5 to 3
move 24 from 6 to 9
move 6 from 3 to 5
move 14 from 7 to 9
move 1 from 4 to 1
move 20 from 9 to 7
move 9 from 3 to 8
move 15 from 9 to 6
move 1 from 5 to 8
move 1 from 2 to 3
move 14 from 6 to 3
move 2 from 3 to 4
move 2 from 3 to 6
move 13 from 7 to 1
move 8 from 3 to 5
move 1 from 3 to 9
move 8 from 5 to 4
move 4 from 5 to 2
move 10 from 1 to 3
move 6 from 4 to 5
move 4 from 5 to 1
move 3 from 1 to 6
move 7 from 8 to 2
move 4 from 4 to 3
move 13 from 3 to 6
move 3 from 8 to 1
move 3 from 7 to 8
move 3 from 8 to 4
move 1 from 4 to 2
move 2 from 3 to 4
move 1 from 5 to 7
move 4 from 7 to 1
move 2 from 3 to 5
move 3 from 2 to 1
move 1 from 4 to 7
move 7 from 2 to 4
move 2 from 4 to 3
move 1 from 7 to 5
move 4 from 9 to 5
move 1 from 4 to 2
move 3 from 2 to 9
move 8 from 1 to 7
move 1 from 3 to 5
move 7 from 5 to 7
move 10 from 6 to 4
move 1 from 5 to 1
move 4 from 1 to 3
move 9 from 7 to 6
move 3 from 1 to 8
move 12 from 4 to 6
move 5 from 4 to 6
move 2 from 9 to 3
move 3 from 8 to 7
move 1 from 1 to 3
move 3 from 7 to 8
move 5 from 7 to 5
move 1 from 7 to 5
move 2 from 3 to 1
move 2 from 8 to 7
move 3 from 5 to 1
move 1 from 9 to 7
move 1 from 8 to 3
move 4 from 7 to 8
move 4 from 5 to 9
move 4 from 1 to 7
move 3 from 8 to 6
move 1 from 8 to 1
move 1 from 7 to 1
move 1 from 5 to 8
move 1 from 8 to 7
move 7 from 3 to 1
move 3 from 9 to 1
move 1 from 9 to 3
move 28 from 6 to 3
move 3 from 7 to 8
move 2 from 8 to 2
move 1 from 2 to 7
move 2 from 6 to 1
move 18 from 3 to 9
move 5 from 3 to 4
move 2 from 7 to 4
move 2 from 1 to 8
move 1 from 2 to 6
move 7 from 6 to 4
move 4 from 4 to 3
move 3 from 8 to 1
move 4 from 9 to 8
move 1 from 4 to 8
move 9 from 1 to 6
move 5 from 1 to 3
move 4 from 6 to 7
move 7 from 6 to 3
move 5 from 8 to 1
move 12 from 3 to 6
move 7 from 6 to 4
move 4 from 3 to 5
move 5 from 6 to 7
move 12 from 4 to 3
move 6 from 1 to 4
move 4 from 4 to 2
move 14 from 9 to 8
move 17 from 3 to 2
move 5 from 4 to 9
move 1 from 9 to 6
move 5 from 2 to 1
move 1 from 9 to 8
move 5 from 1 to 6
move 2 from 2 to 6
move 12 from 2 to 4
move 6 from 7 to 2
move 3 from 7 to 6
move 3 from 9 to 8
move 5 from 4 to 7
move 4 from 2 to 6
move 3 from 6 to 8
move 5 from 8 to 2
move 7 from 6 to 8
move 1 from 7 to 3
move 6 from 4 to 3
move 1 from 8 to 1
move 1 from 5 to 7
move 2 from 6 to 8
move 13 from 8 to 2
move 3 from 5 to 4
move 1 from 1 to 2
move 3 from 6 to 2
move 1 from 1 to 4
move 4 from 4 to 8
move 8 from 3 to 1
move 2 from 4 to 8
move 15 from 2 to 4
move 16 from 8 to 3
move 1 from 8 to 6
move 1 from 7 to 2
move 8 from 1 to 2
move 1 from 6 to 8
move 6 from 3 to 1
move 3 from 3 to 8
move 6 from 3 to 1
move 6 from 2 to 9
move 2 from 1 to 4
move 1 from 8 to 5
move 8 from 2 to 9
move 8 from 1 to 4
move 3 from 8 to 6
move 21 from 4 to 7
move 1 from 9 to 7
move 2 from 6 to 8
move 1 from 5 to 1
move 1 from 3 to 9
move 8 from 9 to 4
move 1 from 1 to 7
move 1 from 1 to 4
move 1 from 6 to 8
move 1 from 9 to 3
move 2 from 9 to 5
move 2 from 5 to 3
move 1 from 9 to 4
move 3 from 8 to 2
move 1 from 1 to 4
move 4 from 4 to 9
move 3 from 3 to 2
move 5 from 9 to 1
move 17 from 7 to 1
move 1 from 9 to 1
move 2 from 2 to 4
move 1 from 4 to 2
move 8 from 2 to 9
move 5 from 4 to 5
move 6 from 4 to 8
move 20 from 1 to 6
move 2 from 9 to 8
move 1 from 2 to 9
move 2 from 8 to 7
move 8 from 7 to 8
move 4 from 5 to 9
move 14 from 8 to 7
move 1 from 5 to 7
move 7 from 9 to 1
move 3 from 6 to 4
move 3 from 9 to 7
move 12 from 6 to 7
move 22 from 7 to 9
move 2 from 2 to 5
move 10 from 1 to 7
move 1 from 4 to 1
move 2 from 6 to 1
move 1 from 1 to 3
move 2 from 4 to 8
move 2 from 8 to 6
move 1 from 3 to 8
move 1 from 4 to 1
move 2 from 5 to 3
move 1 from 8 to 4
move 2 from 3 to 7
move 19 from 9 to 7
move 1 from 1 to 4
move 2 from 9 to 1
move 2 from 1 to 6
move 1 from 6 to 5
move 42 from 7 to 8
move 1 from 7 to 6
move 2 from 4 to 8
move 7 from 6 to 8
move 2 from 1 to 5
move 2 from 9 to 5
move 14 from 8 to 3
move 22 from 8 to 2
move 3 from 5 to 6
move 10 from 8 to 6
move 5 from 8 to 9
move 12 from 6 to 7
move 2 from 5 to 1
move 5 from 3 to 2
move 7 from 3 to 5
move 2 from 5 to 1
move 2 from 3 to 7
move 4 from 1 to 2
move 1 from 5 to 7
move 1 from 5 to 4
move 1 from 6 to 2
move 1 from 9 to 2
move 9 from 7 to 3
move 1 from 4 to 1
move 3 from 7 to 5
move 4 from 3 to 2
move 5 from 2 to 3
move 2 from 5 to 2
move 34 from 2 to 9
move 1 from 1 to 5
move 15 from 9 to 3
move 2 from 3 to 2
move 1 from 5 to 4
move 7 from 3 to 8
move 3 from 9 to 2
move 6 from 9 to 4
move 5 from 9 to 3
move 4 from 4 to 6
move 1 from 6 to 8
move 1 from 3 to 5
move 6 from 3 to 2
move 1 from 4 to 9
move 2 from 4 to 2
move 4 from 5 to 8
move 1 from 5 to 6
move 1 from 7 to 6
move 1 from 9 to 6
move 1 from 7 to 2
move 12 from 8 to 7
move 2 from 7 to 3
move 4 from 6 to 9
move 7 from 9 to 4
move 9 from 3 to 9
move 11 from 7 to 4
move 3 from 9 to 6
move 1 from 4 to 1
move 15 from 4 to 3
move 2 from 4 to 1
move 3 from 1 to 4
move 17 from 3 to 7
move 4 from 3 to 7
move 7 from 9 to 2
move 3 from 4 to 1
move 4 from 6 to 9
move 1 from 9 to 6
move 1 from 3 to 1
move 5 from 7 to 9
move 8 from 9 to 4
move 1 from 1 to 6
move 6 from 4 to 9
move 4 from 2 to 3
move 1 from 4 to 3
move 1 from 4 to 9
move 1 from 1 to 7
move 1 from 7 to 9
move 3 from 6 to 2
move 9 from 2 to 3
move 1 from 9 to 4
move 1 from 1 to 5
move 12 from 7 to 6
move 4 from 9 to 8",
    )
}
