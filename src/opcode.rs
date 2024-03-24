#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpCode {
    CONSTANT,
    RETURN ,
    
}


impl From<u8> for OpCode {
    fn from(value: u8) -> Self {
        match value {
            0 => OpCode::CONSTANT,
            1 => OpCode::RETURN,
            _ => panic!("Invalid OpCode value: {}", value),
        }
    }
}