"""Tests for RBAC Module"""

import pytest
from rbac.rbac_filter import RBACFilter

def test_admin_access():
    """Admin should access all departments"""
    rbac = RBACFilter()
    assert rbac.can_access("admin", ["finance"])
    assert rbac.can_access("admin", ["engineering"])

def test_finance_access():
    """Finance user should only access finance"""
    rbac = RBACFilter()
    assert rbac.can_access("finance", ["finance"])
    assert not rbac.can_access("finance", ["engineering"])

def test_employee_access():
    """Employee should only access general"""
    rbac = RBACFilter()
    assert rbac.can_access("employee", ["employee"])
    assert not rbac.can_access("employee", ["finance"])
