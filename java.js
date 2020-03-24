function cakes(recipe, available) {
    const newRecipe = JSON.parse(JSON.stringify(recipe))
    const newAvail = JSON.parse(JSON.stringify(available))
    if(Object.keys(newRecipe).length > Object.keys(newAvail).length) {
        return 0
    }
    let count = 0

    while (true) {
        for (item in newAvail) {
            if(newRecipe.hasOwnProperty(item) && newAvail[item] - newRecipe[item] > 0) {
                newAvail[item] -= newRecipe[item]
            } else {
                break
            }
        }
        if(Object.values(newAvail).some(item => item <= 0)) {
            break;
        }
        count += 1
    }
    return count
}

// cakes({apples: 3, flour: 300, sugar: 150, milk: 100, oil: 100}, {sugar: 500, flour: 2000, milk: 2000})
console.log(cakes({flour: 500, sugar: 200, eggs: 1}, {flour: 1200, sugar: 1200, eggs: 5, milk: 200}))