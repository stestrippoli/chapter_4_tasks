use std::cmp::{min, Ordering};
use std::fmt::{Display, Formatter, Result};
use std::fs::File;
use std::io::{self, BufRead, BufReader, Error};
use std::ops::Sub;

struct Calendar<T> {
    schedule: Vec<(T, T)>,
    bounds: (T, T),
}

impl<T> Calendar<T> {
    fn new(schedule: Vec<(T, T)>, bounds: (T, T)) -> Self {
        Calendar {
            schedule,
            bounds,
        }
    }

    fn from(path: &str) -> Result<Self, Error> {
        let input = File::open(path)?;
        let reader = BufReader::new(input);

        let line = reader.lines().next().ok_or(io::Error::new(
            io::ErrorKind::InvalidData,
            "Invalid input format",
        ))??;
        let time: Vec<i32> = line
            .trim()
            .split(':')
            .map(|s| s.parse().unwrap())
            .collect();
        let d1 = Date::new(time[0], time[1]);

        let line = reader.lines().next().ok_or(io::Error::new(
            io::ErrorKind::InvalidData,
            "Invalid input format",
        ))??;
        let time: Vec<i32> = line
            .trim()
            .split(':')
            .map(|s| s.parse().unwrap())
            .collect();
        let d2 = Date::new(time[0], time[1]);

        let bounds = (d1, d2);

        let schedule: Vec<(Date, Date)> = reader
            .lines()
            .map(|line| {
                let line = line.unwrap();
                let time: Vec<i32> = line
                    .trim()
                    .split(':')
                    .map(|s| s.parse().unwrap())
                    .collect();
                let d1 = Date::new(time[0], time[1]);

                let line = reader.lines().next().unwrap().unwrap();
                let time: Vec<i32> = line
                    .trim()
                    .split(':')
                    .map(|s| s.parse().unwrap())
                    .collect();
                let d2 = Date::new(time[0], time[1]);

                (d1, d2)
            })
            .collect();

        Ok(Calendar::new(schedule, bounds))
    }
}

struct Date {
    h: i32,
    m: i32,
}

impl Date {
    fn new(h: i32, m: i32) -> Self {
        Date { h, m }
    }
}

impl Display for Date {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{:02}:{:02}", self.h, self.m)
    }
}

impl Ord for Date {
    fn cmp(&self, other: &Self) -> Ordering {
        self.h.cmp(&other.h).then(self.m.cmp(&other.m))
    }
}

impl PartialOrd for Date {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for Date {
    fn eq(&self, other: &Self) -> bool {
        self.h == other.h && self.m == other.m
    }
}

impl Eq for Date {}

impl Sub for Date {
    type Output = Date;

    fn sub(self, rhs: Self) -> Self::Output {
        let minutes = (self.h * 60 + self.m) - (rhs.h * 60 + rhs.m);
        Date {
            h: minutes / 60,
            m: minutes % 60,
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let c1 = Calendar::from(&args[1]).unwrap();
    let c2 = Calendar::from(&args[2]).unwrap();
    let int = args[3].parse::<i32>().unwrap();
    let intd = Date::new(int / 60, int % 60);

    let s1 = c1.bounds.0;
    let e1 = c1.bounds.1;
    let s2 = c2.bounds.0;
    let e2 = c2.bounds.1;

    let mut i1 = c1.schedule.iter().peekable();
    let mut i2 = c2.schedule.iter().peekable();

    let mut s = Date::new(0, 0);
    if s1 >= s2 {
        s = s1;
        loop {
            let b1 = i1.peek().copied().unwrap_or(&e1);
            let b2 = i2.peek().copied().unwrap_or(&e2);

            let b = min(b1.0, b2.0);
            if b - s > intd {
                println!("{} {}", s, b)
            }
            s = max(b1.1, b2.1);

            if i1.next().is_none() && i2.next().is_none() {
                break;
            }
        }
    }
}