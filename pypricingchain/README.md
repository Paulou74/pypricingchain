# pypricingchain

pybacktestchain was cool, but it was missing a pricing feature ...

## Installation

```bash
$ pip install pypricingchain
```

## Usage

pypricing is a package built on top of pybacktestchain, meaning that all the functionalities are still available for use here. pypricingchain leverages several functionalities previously developed, and adds the possibility to price autocallable equity products, using a user-friendly interface developed with Streamlit. The package offers an interesting opportunity to price simultaneously 2 products with different features. Alongside the difference in prices, a visual understanding of these differences is made available by displaying the simulated trajectories used for the pricings, making it visually easy to explain pricing differences depending on pricing inputs.

To use my package, create a python file (i.e. name.py) containing the following lines

```python
from pypricingchain.launch_app import launch_app

if __name__ == "__main__":
    launch_app()
```

then type the following command in a terminal (make sure the terminal is in the same file directory as name.py)

### Important: Make sure you verify the YahooFinance tickers to make sure the pricing runs smoothly.

```bash
$ streamlit run name.py
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pypricingchain` was created by Louis Schiele. It is licensed under the terms of the MIT license.

## Credits

`pypricingchain` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
