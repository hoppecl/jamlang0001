let a = "global";
{
    let showA = fn() {
        print(a);
    };

    print(a);
    showA(1);
    let a = "local";
    showA(1);
    print(a);
};