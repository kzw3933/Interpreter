#[macro_export]
macro_rules! impl_from_u8_for_enum {
    ($(#[$meta: meta])* $vis: vis enum $name: ident {
        $($(#[$imeta: meta])* $iname: ident $(= $val: expr)?,)*
    }) => {
        $(#[$meta])*
        $vis enum $name {
            $($(#[$imeta])* $iname $(= $val)?,)*
        }
        impl From<u8> for $name {

            fn from(v:  u8) -> Self {
                match v {
                    $(x if x == $name::$iname as u8 => $name::$iname,)*
                    _ => panic!("Unexpected value: u8 for enum"),
                }
            }
        }
    }
}


#[macro_export]
macro_rules! define_const {
    ($name: ident, $value: expr, $ty: ty) => {
        const $name: $ty = $value;
    };
}
