let a = "global";
{
    let showA = fn() {
        print(a);
    };

    print(a);
    showA();
    let a = "local";
    showA();
    print(a);
};