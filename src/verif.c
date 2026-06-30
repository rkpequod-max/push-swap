/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   verif.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int		ordered(t_pile *head, int ascendant)
{
	if (head && head->next)
	{
		if (head->x < head->next->x || ascendant)
			while (head->next)
			{
				if (head->x > head->next->x)
					return (0);
				head = head->next;
			}
		else if (head->x > head->next->x)
			while (head->next)
			{
				if (head->x < head->next->x)
					return (0);
				head = head->next;
			}
		else
			ordered(head->next, ascendant);
	}
	return (1);
}

int		count_between(t_pile *p, int min, int max)
{
	int count;

	count = 0;
	while (p)
	{
		if (min <= p->x && p->x <= max)
			count++;
		p = p->next;
	}
	return (count);
}

int		median_between(t_pile *p, int min, int max)
{
	t_pile	*copy;
	int		size;
	int		x;

	copy = NULL;
	size = 0;
	while (p)
	{
		if (min <= p->x && p->x < max)
		{
			size++;
			push(&copy, p->x);
		}
		p = p->next;
	}
	x = find_median(copy, size / 2 + 1);
	free_pile(&copy);
	return (x);
}

int		find_median(t_pile *head, int k)
{
	t_pile	*l;
	t_pile	*r;
	int		median;
	int		x;

	l = NULL;
	r = NULL;
	median = head->x;
	if (pile_len(head) == 1)
		return (median);
	head = head->next;
	while (head)
	{
		push((head->x < median) ? &l : &r, head->x);
		head = head->next;
	}
	if (pile_len(l) == k - 1)
		x = median;
	else if (pile_len(l) > k - 1)
		x = find_median(l, k);
	else
		x = find_median(r, k - pile_len(l) - 1);
	free_pile(&l);
	free_pile(&r);
	return (x);
}

int		free_split(char **strs)
{
	int i;

	i = 0;
	while (strs[i])
		free(strs[i++]);
	free(strs[i]);
	free(strs);
	return (0);
}
