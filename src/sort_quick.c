/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_quick.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int		sab(t_pile **p, char *str, int op)
{
	int tmp;
	int tmp2;

	if (*p && (*p)->next)
	{
		ft_putstr(str);
		tmp = (*p)->x;
		tmp2 = (*p)->next->x;
		pop(p);
		pop(p);
		push(p, tmp);
		push(p, tmp2);
	}
	if (!ft_strcmp(str, "sa\n") && op == 0)
		print_pile(*p);
	return (1);
}

int		pab(t_pile **p1, t_pile **p2, char *str, int op)
{
	if (*p1)
	{
		ft_putstr(str);
		push(p2, (*p1)->x);
		pop(p1);
	}
	if (!ft_strcmp(str, "pa\n") && op == 0)
		print_pile(*p2);
	return (1);
}

int		rrab(t_pile **head, char *str, int op)
{
	t_pile	*last_node;
	t_pile	*prev_node;

	if (*head == NULL || (*head)->next == NULL)
		return (1);
	ft_putstr(str);
	last_node = *head;
	prev_node = NULL;
	while (last_node->next)
	{
		prev_node = last_node;
		last_node = last_node->next;
	}
	push(head, last_node->x);
	free(last_node);
	prev_node->next = NULL;
	if (!ft_strcmp(str, "rra\n") && op == 0)
		print_pile(*head);
	return (1);
}

int		rab(t_pile **head, char *str, int op)
{
	t_pile	*last_node;

	if (*head == NULL || (*head)->next == NULL)
		return (1);
	ft_putstr(str);
	last_node = *head;
	while (last_node->next)
		last_node = last_node->next;
	last_node->next = new_node((*head)->x, NULL);
	pop(head);
	if (!ft_strcmp(str, "ra\n") && op == 0)
		print_pile(*head);
	return (1);
}

void	solve_it(t_pile **pa, t_pile **pb, int n, t_pivot v)
{
	int pivot;
	int tmp;

	if (ordered(*pa, 1) && !(*pb))
		return ;
	if (count_between((n) ? *pa : *pb, v.min, v.max) > 2)
	{
		pivot = (n) ? move_pivot(pa, pb, 1, v) : 0;
		(n == 2) ? quick_return(pa, v) : 0;
		pivot = (!n) ? move_pivot(pb, pa, 0, v) : pivot;
		tmp = v.max;
		v.max = pivot;
		solve_it(pa, pb, 0, v);
		v.max = tmp;
		v.min = pivot;
		solve_it(pa, pb, 2, v);
	}
	else
	{
		if (pile_len(*pb) > 1 && ((*pb)->x < (*pb)->next->x))
			sab(pb, "sb\n", v.op);
		pab(pb, pa, "pa\n", v.op);
		if (*pb)
			pab(pb, pa, "pa\n", v.op);
	}
}
