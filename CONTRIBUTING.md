# Contributing to `sportypy`

First of all, thanks for considering contributing to `sportypy`! The package, just like all open source projects, can't improve without contributions and feedback from its users.

`sportypy` is a labor of love, and no one is being paid to work on it. Please keep this in mind throughout your contributions, as responses and bug fixes may take a bit of time to work through.

## Play by the Rules - Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE-OF-CONDUCT.md). By participating in this project, you're agreeing to abide by its terms.

`sportypy`'s League Office (see below) reserves the right to limit and/or exclude contributions from those who violate the Code of Conduct as is appropriate.

## Getting In The Game - Making Contributions

There's many ways that you can contribute to `sportypy`. If you want a more complete explanation of how you can contribute (to any open source project, not just this one), check out [this guide](https://opensource.guide/how-to-contribute/).

### Be A Fan - Love the Package

Think that `sportypy` is awesome? Want to share the awesome plots and gifs you made with it? Let others discover it by telling them in person, tagging the project on [Twitter](https://www.twitter.com/sportypy), or writing a blog post about your experience with it!

If you're using `sportypy` in an academic context, please do your best to cite the package as well.

### Scouting Reports - Bugs and Feature Suggestions

Like any good sports organization, `sportypy` does its best to scout for itself and solve problems before they become problems. Given a tough test, problems are sure to arise. They can be overcome in their next match, however, by making use of good scouting (bug) reports. Please create an [Issue](https://github.com/sportsdataverse/sportypy/issues) when you find something that needs to be fixed. Here's a good general guide to follow for creating one:

1) Please double check the [README](https://www.github.com/sportsdataverse/sportypy) and the [Issues](https://github.com/sportsdataverse/sportypy/issues) pages to be sure that your problem hasn't already been solved. This isn't meant to stop you from reporting your problem, but rather to be sure that it's a new one so it can be properly addressed.

2) Title your issue with a clear description of what you're looking for. Titling your Issue "This is weird..." doesn't give as good of an idea of what you're after as titling your Issue "NCAA Football hashmarks are out of place." Even better if you can prefix/tag your Issue with `bug` or `feature-request`

3) Spend some time creating a detailed explanation, with a reproducible example, of the problem you're having. Without being able to understand the issue, it's even harder to find what's causing it to occur. Do your best to make sure your code is well-formatted and easy for others to read:

    - Make sure you name your variables something informative

    - Use comments to indicate where you believe the problem in your code is occurring

    - Only include the necessary code to recreate the problem in your Issue report so it can be solved correctly

### The League Office Directory - Contributor Status

Want to join `sportypy`'s team and help shape the package? Great! We're always recruiting! Here's how you can join:

- **League Office** &mdash; By contributing regularly, providing substantial upgrades to the package's overall structure and function, and helping to maintain the package across the board, you'll be considered for membership in the `sportypy`'s **League Office**.

    In order to join the League Office, you must be invited by a current member and get approved by a majority of the other members of the League Office

    When you become a League Officer, you should list yourself in the [README](https://github.com/sportsdataverse/sportypy)

- **General Managers** &mdash; Writing the code that extends `sportypy`'s sport-plotting reach by developing for new sports will earn you a spot as a **General Manager**. Please list yourself (in alphabetical-by-sport order) in the [README](https://github.com/sportsdataverse/sportypy) with what sport you've added.

    Note that by contributing a new sport, you'll be considered the General Manager of that sport. You may be asked to assist in sport-specific issues if the League Office is unable to provide a clear answer

- **Coaching Staffs** &mdash; Patching a bug in an already-existing sport means you're eligible to be on that sport's **coaching staff**. You've got your eye on the game, and it's much appreciated! Coaches can list themselves in the [README](https://github.com/sportsdataverse/sportypy) as well, similar to how General Managers are listed

- **Scout Team** &mdash; By fixing a typo, making a slight modification to something that already exists in `sportypy`, or regularly reporting issues with the package that you encounter (or even helping others solve theirs), you can join the **Scout Team**. Thanks for being on the front lines of the package's operation! Feel free to list yourself in the [README](https://github.com/sportsdataverse/sportypy) under **Scout Team** with a brief description of your role ("Typo Fixer" or "Question Answerer" work great, but be as creative with it as you'd like)

## Becoming a Coach/General Manager - Pull Request Process

To become a Cocah or General Manager, submit a [Pull Request](https://github.com/sportsdataverse/sportypy/pulls) (PR) on GitHub using this process:

1) Create a branch in git and make the changes you wish to see implemented

2) Push your branch to GitHub and open your PR. Your PR should be titled in a way that it's obvious what it's overarching goal is

3) Discuss the PR in as much detail as possible. Provide links to your sources, and clearly explain why the PR is necessary and how it can be used. Any deviations from the conventions of the rest of the package should be clearly explained, but only if the deviation is necessary

4) Continue iterating your request until the League Office determines if the addition is a good fit for `sportypy`

Your request will be checked against the following points:

- **Motivation** &mdash; Clearly and concisely explain what motivated the PR. If it addresses a particular issue, be sure you link to it

- **Only Related Changes** &mdash; Before you submit your PR, make sure your PR only addresses *one* issue. If you want to fix multiple issues, please address them in separate PRs so that it's clear what change is being made in each PR. Please also be sure that your PR doesn't introduce any new bugs or break any existing code

- **Code Style and File Naming** &mdash; Please follow [the flake8 styleguide](https://flake8.pycqa.org/en/latest/). Maintaining consistent styling facilitates easier current maintenance and future development.

    Additionally, please keep consistent with the naming of new files, especially when adding a new sport. Files that contain a new sport's features should be added to the `sportypy/_features/` directory, and the base surface (and any child classes for specific leagues) to the `sportypy/surfaces` directory. Dimensions should be maintained in the `sportypy/data/raw/surface_dimensions.json` file. Please parameterize the surface to the best of your abilities, and ask with any questions!

- **Documentation** &mdash; When introducing new code, please make sure you document it appropriately. Documentation comes in three main forms:

  - Docstrings for classes and their sub-methods. These should include markdown syntax as the documentation page for the package website uses markdown rendering

  - In the `docs/` subdirectory which renders the package website. Be sure to add your sport and any supported leagues/child classes to the following files:

    - `docs/features/{your sport}.md` &mdash; A file to document the features for the sport you're adding

    - `docs/surfaces/{your sport}/{league name}.md` &mdash; One file per league, meant as the simplest interface to the package

    - `docs/surfaces/{your sport}.md` &mdash; Be sure to add a new file here to document your sport, listing all of the leagues alphabetically. These should reference the files in the bullet above

    - `docs/features.md` &mdash; Please add your sport alphabetically in the list following the existing examples

    - `docs/surfaces.md` &mdash; Please add your sport alphabetically in the list following the existing examples

  - In-line/in-file comments throughout the code that explain what your code is trying to achieve

    If this is confusing, take a look at the existing structure here for examples. Most of this can be copied from sport to sport.

- **Testing** &mdash; `sportypy` relies upon extensive testing to ensure that the package runs smoothly. It currently has 100% code coverage, and your PR should ensure that this remains the case.

    To test your coverage, be sure to have the `pytest` package installed and run the following commands:

    ```bash
    pip install pytest
    pytest --cov=sportypy tests/ --cov-config=.coveragerc --cov-report=term
    ```

    This will show you where your new code lacks sufficient coverage, so please be sure to add tests in the `tests/` repository to make sure you're covered! For help on creating tests, please reach out to the League Office

Although this seems like a lot of work and a big hassle, the League Office doesn't expect perfection and is on hand to help out as needed.
