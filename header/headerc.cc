#include <errno.h>
#include <zlib.h>


//=================================================================================================

#include <vector>

#include <python2.7/Python.h>
#include <stdlib.h>
#include <cstring>

using namespace std;

struct Singu{
    vector<int> val; 
    bool friend operator == (const Singu &self, const Singu &other){
        if(self.val.size() != other.val.size())
            return false;
        for(int i = 0; i < self.val.size(); ++i){
            if(self.val[i] != other.val[i])
                return false;
        }
        return true;
    }
};

struct Atom{
    vector<struct Singu> val;
};

struct Molecule{
    vector<struct Atom> val;
    Molecule(){}
    Molecule(vector<struct Atom> &other) : val(other){
    }
};

static struct Molecule *moleculeFromPy(PyObject *mole)
{
    struct Molecule *ret_mole = new Molecule();
    int n_molecule = PyList_Size(mole);

    for(int i = 0; i < n_molecule; ++i){
        PyObject *atom = PyList_GetItem(mole, i);
        int n_atom = PyList_Size(atom);
        struct Atom ret_atom;

        for(int j = 0; j < n_atom; ++j){
            PyObject *singu = PyList_GetItem(atom, j);
            int n_singu = PyList_Size(singu);
            struct Singu ret_singu;

            for(int k = 0; k < n_singu; ++k){
                PyObject *val = PyList_GetItem(singu, k);
                int value;
                PyArg_Parse(val, "i", &value);

                ret_singu.val.push_back(value);
            }
            ret_atom.val.push_back(ret_singu);
        }
        ret_mole->val.push_back(ret_atom);
    }
    return ret_mole;
}

static PyObject* moleculeToPy(struct Molecule *mole)
{
    PyObject *ret_mole = PyList_New(mole->val.size());
    for(int i = 0; i < mole->val.size(); ++i){
        struct Atom& atom = mole->val[i];
        PyObject *ret_atom = PyList_New(atom.val.size());

        for(int j = 0; j < atom.val.size(); ++j){
            struct Singu& singu = atom.val[j];
            PyObject *ret_singu = PyList_New(singu.val.size());

            for(int k = 0; k < singu.val.size(); ++k){
                PyList_SetItem(ret_singu, k, Py_BuildValue("i",singu.val[k]));
            }
            PyList_SetItem(ret_atom, j, ret_singu);
        }
        PyList_SetItem(ret_mole, i, ret_atom);
    }
    return ret_mole;
}

struct Singu *intersect_singu(struct Singu *singu1, struct Singu *singu2)
{
    struct Singu *ret_singu = new Singu();
    for(int i = 0; i < singu1->val.size(); ++i)
    {
        int a = singu1->val[i];
        int b = singu2->val[i];
        if(a == b)
            ret_singu->val.push_back(a);
        else if(a == -1)
            ret_singu->val.push_back(b);
        else if(b == -1)
            ret_singu->val.push_back(a);
        else{
            delete ret_singu;
            return NULL;
        }
    }
    return ret_singu;
}

struct Atom *intersect_atom(struct Atom *atom1, struct Atom *atom2)
{
    struct Atom *ret_atom;
    struct Singu *domain = intersect_singu(&(atom1->val[0]), &(atom2->val[0]));
    
    if(domain == NULL)
        return NULL;

    ret_atom = new Atom();
    ret_atom->val.push_back(*domain);
    for(int i = 1; i < atom1->val.size(); ++i){
        struct Singu *temp = intersect_singu(domain, &(atom1->val[i]));
        if(temp != NULL){
            ret_atom->val.push_back(*temp);
        }
    }
    for(int i = 1; i < atom2->val.size(); ++i){
        struct Singu *temp = intersect_singu(domain, &(atom2->val[i]));
        if(temp != NULL){
            ret_atom->val.push_back(*temp);
        }
    }

    for(int i = 1; i < ret_atom->val.size(); ++i){
        if(ret_atom->val[i] == ret_atom->val[0]){
            delete ret_atom;
            return NULL;
        }
    }
    return ret_atom;
}
void printSingu(struct Singu *singu)
{
    printf("Singu len: %d\n",singu->val.size());
    for(int i = 0; i < singu->val.size(); ++i){
        printf("%d, ",singu->val[i]);
    }
    printf("\n");
}
void printAtom(struct Atom *atom)
{
    printf("atom len: %d\n",atom->val.size());
    for(int i = 0; i < atom->val.size(); ++i){
        printSingu(&(atom->val[i]));
    }
}
void printMole(struct Molecule *mole)
{
    printf("mole len: %d\n",mole->val.size());
    for(int i = 0; i < mole->val.size(); ++i){
        printAtom(&(mole->val[i]));
    }
}

static PyObject *header_intersect_molecule(PyObject *self, PyObject *args)
{
    PyObject *args_temp = PySequence_GetItem(args, 0);
    if(PySequence_Size(args_temp) != 2)
        Py_RETURN_NONE;
    PyObject *molecule1 = PySequence_GetItem(args_temp, 0);
    PyObject *molecule2 = PySequence_GetItem(args_temp, 1);

    // check the input;
    struct Molecule *mole1 = moleculeFromPy(molecule1);
    struct Molecule *mole2 = moleculeFromPy(molecule2);
    //printf("len1: %d\n",mole1->val.size());
    //printMole(mole1);
    //printMole(mole2);
    
    // intersect_molecule algorithm. 
    struct Molecule *ret_mole = new Molecule(); 

    for(int i = 0; i < mole1->val.size(); ++i){
        for(int j = 0; j < mole2->val.size(); ++j){
            struct Atom *ret_atom = intersect_atom(&(mole1->val[i]), &(mole2->val[j]));
            if(ret_atom != NULL)
                ret_mole->val.push_back(*ret_atom);
        }
    }

    // return the result;
    if(ret_mole->val.size() == 0)
        Py_RETURN_NONE;

    PyObject *ret = moleculeToPy(ret_mole);
    delete ret_mole;
    return ret;
}
static bool include_singu(struct Singu *a, struct Singu *b)
{
    for(int i = 0; i < a->val.size(); ++i){
        if(a->val[i] != b->val[i] && a->val[i] != -1)
            return false;
    }
    return true;
}
static struct Molecule *header_subtract_atom(struct Atom *atomA, struct Atom *atomB)
{
    if(atomA->val.size() == 0
        || atomB->val.size() == 0)
        return NULL;
    struct Singu *domain = intersect_singu(&(atomA->val[0]), &(atomB->val[0]));
    
    // ?
    for(int i = 1; i <  atomA->val.size(); ++i){
        if(include_singu(&(atomA->val[i]), domain)){
            delete domain;
            return NULL;
        }
    }

    struct Molecule *ret_mole = new Molecule();
    struct Atom *atom = new Atom();
    if(include_singu(domain, &(atomA->val[0])) == false){
        atom->val.push_back(atomA->val[0]);
        atom->val.push_back(*domain);
        for(int i = 1; i < atomA->val.size(); ++i){
            if(include_singu(domain, &(atomA->val[i])) == false){
                atom->val.push_back(atomA->val[i]);
            }
        }
        ret_mole->val.push_back(*atom);
    }
    delete atom;

    for( int i = 1; i < atomB->val.size(); ++i){
        struct Singu *atomMain = intersect_singu(&(atomB->val[i]), &(atomA->val[0]));
        if(atomMain == NULL){
            delete atomMain;
            continue;
        }

        atom = new Atom();
        atom->val.push_back(*atomMain);
        bool valid = true;
        for(int j = 1; j < atomA->val.size(); ++j){
            struct Singu *singu = intersect_singu(atomMain, &(atomA->val[j]));
            if(singu != NULL){
                if(singu == atomMain){
                    valid = false;
                    delete singu;
                    break;
                }
                else{
                    atom->val.push_back(*singu);
                }
            }
            delete singu;
        }
        if(valid){
            ret_mole->val.push_back(*atom);
        }
        delete atom;
    }
    return ret_mole;
}

static Molecule* header_subtract_molecule(struct Molecule *molecule1, struct Molecule *molecule2)
{
    if(molecule1 == NULL)
        return NULL;

    struct Molecule *mole = new Molecule(*molecule1);

    int n_mole = mole->val.size();
    vector<int> counter(n_mole,1);
    int m_mole = molecule2->val.size();
    for(int i = 0; i < mole->val.size(); ++i){
        struct Atom *atom = &(mole->val[i]);
        bool flag = true;
        for(int j = 0; j < m_mole; ++j){
            struct Molecule *cur_mole = header_subtract_atom(atom, &(molecule2->val[j]));
            if(cur_mole != NULL){
                flag = false;
                for(int k = 0; k < cur_mole->val.size(); ++k){
                    mole->val.push_back(cur_mole->val[k]);
                    counter.push_back(1);
                }

                counter[i] = 0;
                delete cur_mole;
                break;
            }
        }
    }
    struct Molecule *ret_mole = new Molecule();
    for(int i = 0; i < mole->val.size(); ++i){
        if(counter[i] == 1){
            ret_mole->val.push_back(mole->val[i]);
        }
    }
    if(ret_mole->val.size() <= 0){
        delete ret_mole;
        return NULL;
    }
    return ret_mole;
}

static PyObject* header_subtract_wrapper(PyObject *self, PyObject *args)
{
    if(PySequence_Size(args) != 2)
        return NULL;
    PyObject *intersection = PySequence_GetItem(args, 0);
    PyObject *header_sapce = PySequence_GetItem(args, 1);

    struct Molecule *subtraction = moleculeFromPy(intersection);

    int n = PyList_Size(header_sapce);
    for(int i = 0; i < n; ++i){
        PyObject *cur = PyList_GetItem(header_sapce, i);
        subtraction = header_subtract_molecule(subtraction, moleculeFromPy(cur));
        if(subtraction->val.size() == 0)
            return NULL;
    }
    PyObject *ret_mole = moleculeToPy(subtraction);
    delete subtraction;
    return ret_mole;
}

static PyMethodDef headercMethods[] = {
    {"intersect_molecule",  header_intersect_molecule, METH_VARARGS,
     "Execute an header space analysis."},
    {"subtract_wrapper",  header_subtract_wrapper, METH_VARARGS,
     "Execute a substract wrapper"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initheaderc(void)
{
    (void) Py_InitModule("headerc", headercMethods);
}
