pub enum Value {
    Number(f64),
}

impl Value {
    pub fn print(&self) {
        match self {
            Self::Number(value) => print!("{}", value),
        }
    }
}

impl From<f64> for Value {
    fn from(value: f64) -> Self {
        Self::Number(value)
    }
}