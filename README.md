# building-generator

This is a building generating module to draw building.
You can get buildings from point of view you set.
![angled_roof](https://github.com/teo646/building-generator/assets/61399931/36be7d3f-2090-4bb8-ba6c-ed6110b82445)
![straight_roof](https://github.com/teo646/building-generator/assets/61399931/879610e8-be6e-4c4c-86ab-4dabe6090e4c)
![Screenshot from 2024-02-09 12-28-39](https://github.com/teo646/building-generator/assets/61399931/55e39621-989f-4a17-81bb-668737b53e46)


This module is based on mask-canvas module i made.
so you have to download it before you use it.

https://github.com/teo646/mask-canvas.git
this is the link for the module

### Prerequisites

cv2, numpy but will be install automatically via pip install -e.

### Installing

1. create virtual environment(venv)
```
python -m venv .venv
source .venv/bin/activate
```

2. install module
```
git clone https://github.com/teo646/building-generator.git
cd building-generator
pip install -e .
```


## Running the tests
```
python example/drawing.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


