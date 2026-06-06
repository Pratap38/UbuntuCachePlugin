import plotext as plt

def showchart(results):
    categories=[]
    size=[]

    for category in results:
        categories.append(
            category.name
        )
        size.append(
            category.size
        )
    plt.clear_data()

    plt.bar(
        categories,
        size
    )

    plt.title(
        "Cache Usage"
    )

    plt.show()
