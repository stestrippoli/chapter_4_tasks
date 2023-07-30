use std::cmp::min;
use std::fmt::Display;
use std::io::{Write, BufReader, BufRead, Error};
use std::fs::File;
struct Calendar<Date> { 
    schedule: Vec<(Date , Date )>, 
    bounds: (Date,Date) 
}

impl Calendar<Date> {
    fn new(schedule : Vec<(Date,Date)>, b: (Date, Date)) -> Self {
        return Calendar { schedule: schedule, bounds: b }
    }

    fn from(path: &str) -> Result<Self, Error> {
        let input = File::open(path)?;
        let mut buffered = BufReader::new(input);
        let mut line = String::new();
        buffered.read_line(&mut line);
        let time : Vec<&str>= line.trim().split(":").collect();
        let h = time[0].parse::<i32>().unwrap();
        let m = time[1].parse::<i32>().unwrap();
        let d1 = Date::new(h,m);
        line.clear();
        println!("{}", d1);
        buffered.read_line(&mut line);
        let time : Vec<&str>= line.trim().split(":").collect();
        let h = time[0].parse::<i32>().unwrap();
        let m = time[1].parse::<i32>().unwrap();
        let d2 = Date::new(h,m);
        line.clear();
        println!("{}", d2);
        let b = (d1,d2);

        let mut s  = Vec::<(Date, Date)>::new();
        
        loop {
            let x = buffered.read_line(&mut line);
            match x {
                Ok(0) => {
                    break;
                },
                Ok(n) => {
                    let time : Vec<&str>= line.trim().split(":").collect();
                    let h = time[0].parse::<i32>().unwrap();
                    let m = time[1].parse::<i32>().unwrap();
                    let d1 = Date::new(h,m);
                    println!("{}", d1);
                    line.clear();
            
                    buffered.read_line(&mut line);
                    let time : Vec<&str>= line.trim().split(":").collect();
                    let h = time[0].parse::<i32>().unwrap();
                    let m = time[1].parse::<i32>().unwrap();
                    let d2 = Date::new(h,m);
                    line.clear();
                    println!("{}", d2);
                    let b = (d1,d2);
                    s.push(b);
                },
                Err(e) => {
                    e;
                }
            }
        }
    
        return Ok(Calendar::new(s, b));


        

    }
}
#[derive(Eq)]
struct Date {
    h : i32,
    m: i32
}

impl Date {
    fn new(h:i32, m:i32)-> Self {
        return  Date {h:h, m:m};
    }

}

impl Display for Date {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut mm = String::from('0');
        let mut hh = String::from('0');
        if self.m < 10 {
            mm.push(self.m.to_string().chars().nth(0).unwrap())
        }
        else{
            mm = self.m.to_string();
        }
        if self.h < 10 {
            hh.push(self.h.to_string().chars().nth(0).unwrap())
        }
        else{
            hh = self.h.to_string();
        }
        write!(f, "{}:{}", hh, mm)
    }
}
impl Ord for Date {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        if self.gt(other){
            return (std::cmp::Ordering::Greater);
        } 
        else if self.eq(other){
            return (std::cmp::Ordering::Equal);
        }
        else {
            return (std::cmp::Ordering::Less)
        };
    }
}

impl PartialOrd for Date {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        if self.gt(other){
            return Some(std::cmp::Ordering::Greater);
        } 
        else if self.eq(other){
            return Some(std::cmp::Ordering::Equal);
        }
        else {
            return Some(std::cmp::Ordering::Less)
        };
    
    }
    fn gt(&self, other: &Self) -> bool {
        if self.h>other.h {
            return true
        }
        else {
            return false
        }
    }
    fn ge(&self, other: &Self) -> bool {
        if self.h>other.h {
            return true
        }
        else {
            if (self.h == other.h) && (self.m > other.m) {
                return true
            }
            else{
                return false
            }        
        }
    }
}

impl PartialEq for Date {
    fn eq(&self, other: &Self) -> bool {
        if (self.m == other.m) && (self.h == other.h) {
            return true;
        }
        else {
            return false
        }
    }
}
use std::{ops::{Sub}};

impl Sub for Date{
    type Output = Date;
    fn sub(self, rhs: Self) -> Date {
        let mut mm = self.m - rhs.m;
        let mut hh=0;
        if mm < 0{
            mm +=60;
            hh=23;
        }
        hh -= self.h - rhs.h;
        if hh < 0{
            hh += 24;
        }
        return Self::new(hh, mm)
    }
}


fn main() {
    let _args : Vec<String> = std::env::args().collect();
    let c1  = Calendar::from(&_args[1]).unwrap();
    let c2  = Calendar::from(&_args[2]).unwrap();
    let int = _args[3].parse::<i32>().unwrap();
    let intd = Date::new(int/60, int%60);
    
    let s1 = c1.bounds.0;
    let e1 = c1.bounds.1;
    let s2 = c2.bounds.0;
    let e2 = c2.bounds.1;

    let mut i1 = c1.schedule.iter();
    let mut i2 = c2.schedule.iter();

    let mut s = Date::new(0,0);
    if s1.ge(&s2) {
        
        s = s1;
        loop {
            let mut b1 = i1.next();
            match b1 {
                None => {
                    b1 = e1;
                },
                Some(b1) => {b1= b1}
            }

            let b2 = i2.next();
            match b2 {
                None => {
                    b2 = e2;
                },
                Some(b2) => {b2.unwrap()}
            }
            let b = min(b1.unwrap().0,b2.unwrap().0).unwrap();
            if b-s > intd {
                println!("{} {}", s, b)
            } 
            s = max(b1.1, b2.1)
        }

        } 
    

    }
    


