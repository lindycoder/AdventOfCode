#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

#[macro_export]
macro_rules! pt {
    ($x:expr, $y:expr) => {
        $crate::tools::points::Point { x: $x, y: $y }
    };
}

#[cfg(test)]
mod tests {
    use crate::tools::points::Point;

    #[test]
    fn test_equals() {
        assert_eq!(pt!(1, 2), pt!(1, 2));
    }

    #[test]
    fn test_copy() {
        let mut p = pt!(1, 2);

        fn f(rp: &Point) -> Point {
            *rp
        }
        let p2 = f(&p);

        assert_eq!(p, p2);
        p.x += 1;
        assert_ne!(p, p2);
    }
}
