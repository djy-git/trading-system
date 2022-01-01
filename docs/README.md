# Documentation using [`SPHINX`](https://www.sphinx-doc.org/en/master/) package
Details are in https://www.sphinx-doc.org/en/master/


# 1. Install `sphinx`
    $ pip install sphinx
    $ pip install sphinx-rtd-theme


# 2. Initialize project settings
    $ sphinx-quickstart docs
    
    // Select default option
    // Write information of the project 
    
    // 한국어 지원이 필요한 경우 다음을 사용
    // Project language [en]: ko


# 3. Modify configurations
## 3.1 `/docs/conf.py`
1. Add root path to `sys.path`
     
       // Existing
       # import os
       # import sys
       # sys.path.insert(0, os.path.abspath('.'))
       
       // Modified
       import os
       import sys
       sys.path.insert(0, os.path.abspath(
           os.path.join(os.path.dirname(__file__), '..')))

2. Add extensions

       // Existing
       extensions = [
       ]
       
       // Modified
       extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.githubpages'
       ]

3. Change html theme

       // Existing
       html_theme = 'alabaster'
       
       // Modified
       html_theme = 'sphinx_rtd_theme'


## 3.2 `/docs/index.rst`
1. Add `modules`
       
       // Existing (Line 9-13)
       .. toctree::
          :maxdepth: 2
          :caption: Contents:
    
       // Modified (Line 9-13)
       .. toctree::
          :maxdepth: 2
          :caption: Contents:
    
          modules
      

# 4. Generate `rst` files (ReStructuredText)
    $ sphinx-apidoc -f -o docs base_structure
    
    
# 5. Build htmls
이후에 파일 구조가 바뀌지 않았다면 build만 해주면 된다.

    $ cd docs
    $ make html
    

# 6. See the generated document in `/docs/_build/html/index.html`


# 7. Whenever new changes occur, repeat steps 4-6
