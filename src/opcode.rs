use crate::impl_from_u8_for_enum;

impl_from_u8_for_enum!(
    #[repr(u8)]
    #[derive(Debug, Clone, Copy, PartialEq)]
    pub enum OpCode {
        constant,
        neg,
        add,
        sub,
        mul,
        div,
        ret,
    }
);