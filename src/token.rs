
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TokenType {
    // single character tokens
    left_paren, right_paren, left_brace, right_brace,
    comma, dot, minus, plus, semicolon, slash, star,
    // one or two characters tokens
    bang, bang_equal, equal, equal_equal,
    greater, greater_equal, less, less_equal,
    // literals
    identifier, string, number,
    // keywords
    and, class, else_, false_, for_, fun, if_, nil, or,
    print, return_, super_, this, true_, var, while_,

    error, eof
}

#[derive(Debug, Clone, Copy)]
pub struct Token {
    pub ty: TokenType,
    pub start: usize,
    pub length: usize,
    pub line: i32,
}