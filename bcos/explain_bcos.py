import torch
import torch.nn as nn
from torch.autograd import Variable

import util

SOFTMAX = nn.Softmax(dim=0)


def explanation_mode(model, active=True):
    for mod in model.modules():
        if hasattr(mod, "explanation_mode"):
            mod.explanation_mode(active)


def explain_domain(model, embedding, test_domain):
    test_domain_pp, _ = util.preprocess_data([test_domain], [0])
    test_domain_pp_tensor = torch.from_numpy(test_domain_pp).cuda()
    test_domain_pp_tensor_transformed = embedding(test_domain_pp_tensor)

    domain = test_domain_pp_tensor_transformed[0]
    _domain = Variable(domain, requires_grad=True)
    _domain = _domain[None, :]

    pred = model(_domain)
    x = (torch.argmax(pred[0]))
    cls = x.item()
    cnf = SOFTMAX(pred[0])[x].item()

    _domain.retain_grad()
    _domain.grad = None
    pred[0][x].backward(retain_graph=True)
    w = _domain.grad

    linearity = ((_domain * w).sum() + model[-1].bias)
    if linearity.shape != ():
        linearity = linearity[x]

    alignment = abs(pred[0][x].item() - linearity.item())

    w_no_padding = torch.squeeze(w)[253 - len(test_domain):]
    x_no_padding = torch.squeeze(_domain)[253 - len(test_domain):]

    con = x_no_padding * w_no_padding
    con = torch.sum(con, dim=1)
    con = torch.div(con, torch.max(torch.abs(con))).cpu().detach().tolist()

    w_no_padding = torch.sum(w_no_padding, dim=1)
    w_no_padding = torch.div(w_no_padding, torch.max(torch.abs(w_no_padding))).cpu().detach().tolist()

    return w_no_padding, con, alignment, cls, cnf
